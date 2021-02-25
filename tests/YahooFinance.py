#! python3
# tests/YahooFinance.py

import unittest

import bs4
import requests


TICKER = "AAPL"
SHEETS = {
    "balance sheet": "balance-sheet",
    "income statement": "financial",
    "cash flow statement": "cash-flow"
}
EXT = SHEETS["blanace sheet"]


class TestClassParser(unittest.TestCase):

    def setUp(self):
        url = f"https://finance.yahoo.com/quote/{TICKER}/{EXT}?p={TICKER}"
        self.res = requests.get(url)
        self.soup = bs4.BeautifulSoup(self.res.text, features="lxml")


if __name__ == '__main__':
    unittest.main()
