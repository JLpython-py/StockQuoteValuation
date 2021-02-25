#! python3
# sqv.CNBC

"""

"""

import logging
import os
import re

import bs4
import requests

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s"
)


URL = "https://apps.cnbc.com/view.asp?symbol={}&uid=stocks/financials{}"
SHEETS = {
    "balance sheet": "",
    "income statement": "&view=incomeStatement",
    "cash flow statement": "&view=cashFlowStatement"
}


class Parser:
    """ Parse financial sheet webpages for financial sheet data
"""
    def __init__(self, ticker, *, report="a", sheet="bs"):
        self.ticker = ticker

        report = report.lower()
        report_aliases = {
            "annual": ["a"], "quarter": ["q"]
        }
        self.report = ""
        for alias in report_aliases:
            if report == alias or report in report_aliases[alias]:
                self.report = alias
                break
        if not self.report:
            raise self.UnknownReportTypeError(report)

        sheet = sheet.lower()
        sheet_aliases = {
            "balance sheet": ["balance", "bs"],
            "income statement": ["income", "is"],
            "cash flow statement": ["cash flow", "cf"]
        }
        self.sheet = ""
        for alias in sheet_aliases:
            if sheet == alias or sheet in sheet_aliases[alias]:
                self.sheet = alias
                break
        if not self.sheet:
            raise self.UnknownSheetTypeError(sheet)

        self.address = URL.format(
            self.ticker, SHEETS[self.sheet]
        )
        if self.report == "annual":
            self.cont = "containerYr"
        else:
            self.cont = "containerQtr"

        self.res = requests.get(self.address)
        self.soup = bs4.BeautifulSoup(self.res.text, features="lxml")

        self.dbpath = os.path.join("data", "CNBC", f"{self.ticker.upper()}.sqlite")

    class UnknownReportTypeError(Exception):

        def __init__(self, report):
            self.report = report
            self.message = f"No financial report '{self.report}'"
            super().__init__(self.message)

    class UnknownSheetTypeError(Exception):

        def __init__(self, sheet):
            self.sheet = sheet
            self.message = f"No financial report sheet '{self.sheet}'"
            super().__init__(self.message)

    def parse(self):
        timeperiods = self.dates()
        content = self.content()
        for con in content:
            content[con] = dict(zip(
                [tp[0] for tp in timeperiods], content[con]
            ))
        return content

    def dates(self):
        """ Retrieve dates from financial report sheet
"""
        selector = f"div[id='{self.cont}'] thead th"
        elems = self.soup.select(selector)[1:]
        if self.report == "annual":
            regex = re.compile(
                r"([0-9]{4})([0-9]{1,2}/[0-9]{1,2}/[0-9]{2})"
            )
        else:
            regex = re.compile(
                r"([0-9]{4} Q[1-4])([0-9]{1,2}/[0-9]{1,2}/[0-9]{2})"
            )
        timeperiods = [
            (regex.search(t).group(1), regex.search(t).group(2))
            for t in [e.getText().strip() for e in elems]
        ]
        return timeperiods

    def content(self):
        """ Retrieve content from financial report sheet
"""
        selector = f"div[id='{self.cont}'] tbody tr"
        rows = self.soup.select(selector)
        content = {}
        for row in rows:
            elems = [e.getText() for e in row.select("td")]
            label, values = elems[0], elems[1:]
            values = self.reformat_values(label, values)
            content.setdefault(label, values)
        return content

    def reformat_values(self, label, values):
        currency, factor = self.get_value_information()
        paren_regex = re.compile(r"\(([0-9,]+)\)")
        grand_regex = re.compile(r"(-?[0-9,]+)K")
        for ind, val in enumerate(values):
            if val == '--':
                continue
            if paren_regex.search(val):
                val = f"-{paren_regex.search(val).group(1)}"
            if grand_regex.search(val):
                val = float(''.join(val.split(','))) * 1e3
            elif "Earning per Common Share" in label:
                val = float(''.join(val.split(',')))
            else:
                val = float(''.join(val.split(','))) * factor
            values[ind] = val
        return values

    def get_value_information(self):
        currency_regex = re.compile(
            r"In (.*)<br />"
        )
        scale_regex = re.compile(
            r"Values are displayed in (.*) except for earnings per share and where noted"
        )
        currency = currency_regex.search(self.res.text).group(1)
        scale = scale_regex.search(self.res.text).group(1)
        numerical = {
            "thousands": 1e3, "millions": 1e6
        }
        factor = numerical[scale.lower()]
        return currency, factor
