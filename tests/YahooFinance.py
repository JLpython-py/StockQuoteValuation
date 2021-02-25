#! python3
# tests/YahooFinance.py

from urllib.request import urlopen
import unittest

from lxml import etree


TICKER = "AAPL"
SHEETS = {
    "balance sheet": "balance-sheet",
    "income statement": "financial",
    "cash flow statement": "cash-flow"
}
EXT = SHEETS["balance sheet"]


class TestClassParser(unittest.TestCase):

    def setUp(self):
        url = f"https://finance.yahoo.com/quote/{TICKER}/{EXT}?p={TICKER}"
        self.response = urlopen(url)
        self.htmlparser = etree.HTMLParser()
        self.tree = etree.parse(self.response, self.htmlparser)

    def test_dates_css_selector(self):
        xpath = "//div[@class='D(tbhg)']//div//div//span"
        elems = self.tree.xpath(xpath)[1:]
        timeperiods = [e.text.strip() for e in elems]
        self.assertTrue(timeperiods)
        self.assertTrue(all([isinstance(t, str) for t in timeperiods]))


if __name__ == '__main__':
    unittest.main()
