#! python3
# sqv.CNBC

"""

"""

import logging
import os
import re

import bs4
import requests

from db import db

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
    def __init__(self, ticker, *, report, sheet):
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
            self.table = "financialReportYr"
        else:
            self.table = "financialReportQtr"

        res = requests.get(self.address)
        self.soup = bs4.BeautifulSoup(res.text, features="lxml")

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
        labels = self.labels()

    def dates(self):
        """ Retrieve dates from financial report sheet
"""
        selector = f"table[id='{self.table}'] thead th"
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

    def labels(self):
        """ Retrieve labels from financial report sheet
"""
        selector = f"table[id='{self.table}'] tr td[class='label']"
        elems = self.soup.select(selector)
        labels = [e.getText().strip() for e in elems]
        return labels
