#! python3
# YahooFinance.py

"""

"""

import logging
import bs4
import requests

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s"
)


URL = "https://finance.yahoo.com/quote/{}/{}?p={}"
SHEETS = {
    "balance sheet": "balance-sheet",
    "income statement": "financial",
    "cash flow statement": "cash-flow"
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
            self.ticker, SHEETS[self.sheet], self.ticker
        )

        self.res = requests.get(self.address)
        self.soup = bs4.BeautifulSoup(self.res.text, features="lxml")

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
