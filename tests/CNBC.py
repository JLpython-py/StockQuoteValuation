#! python3
# tests/CNBC.py

import re
import unittest

import bs4
import requests


TICKER = "AAPL"
SHEETS = {
    "balance sheet": "",
    "income statement": "&view=incomeStatement",
    "cash flow statement": "&view=cashFlowStatement"
}
EXT = SHEETS["balance sheet"]


class TestClassParser(unittest.TestCase):

    def setUp(self):
        url = f"https://apps.cnbc.com/view.asp?symbol={TICKER}&uid=stocks/financials{EXT}"
        self.res = requests.get(url)
        self.soup = bs4.BeautifulSoup(self.res.text, features="lxml")

    def test_dates_css_selector(self):
        selector = "div[id='containerYr'] thead th"
        elems = self.soup.select(selector)[1:]
        timeperiods = [e.getText().strip() for e in elems]
        self.assertTrue(timeperiods)
        self.assertTrue(all([isinstance(t, str) for t in timeperiods]))

    def test_dates_annual_regex(self):
        cases = [
            "202012/31/20", "201912/31/19", "201812/31/18", "201712/31/17"
        ]
        regex = re.compile(
            r"[0-9]{4}[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}"
        )
        self.assertTrue(
            all([regex.search(c) for c in cases])
        )

    def test_dates_quarter_regex(self):
        cases = [
            '2020 Q412/31/20', '2020 Q39/30/20', '2020 Q26/30/20',
            '2020 Q13/31/20', '2019 Q412/31/19'
        ]
        regex = re.compile(
            r"[0-9]{4} Q[1-4][0-9]{1,2}/[0-9]{1,2}/[0-9]{2}"
        )
        self.assertTrue(
            all([regex.search(c) for c in cases])
        )

    def test_content_css_selector(self):
        selector = "div[id='containerYr'] tbody tr"
        rows = self.soup.select(selector)
        self.assertTrue(rows)
        for row in rows:
            elems = [e.getText() for e in row.select("td")]
            self.assertTrue(elems)
            label, values = elems[0], elems[1:]
            self.assertIsInstance(label, str)
            self.assertIsInstance(values, list)
            self.assertTrue(
                all([isinstance(v, str) for v in values])
            )

    def test_reformat_values_regex(self):
        paren_regex = re.compile(r"\(([0-9,]+)\)")
        cases = ["(2,252)", "(1,291)", "(245)"]
        for case in cases:
            self.assertTrue(paren_regex.search(case))

    def test_get_value_information_regex(self):
        self.assertIn(
            "() = Negative Values", self.res.text
        )
        self.assertIn(
            "In U.S. Dollars", self.res.text
        )
        self.assertIn(
            "Values are displayed in Millions except for earnings per share and where noted",
            self.res.text
        )
        currency_regex = re.compile(
            r"In (.*)<br />"
        )
        scale_regex = re.compile(
            r"Values are displayed in (.*) except for earnings per share and where noted"
        )
        self.assertTrue(currency_regex.search(self.res.text))
        self.assertTrue(scale_regex.search(self.res.text))
        self.assertEqual(
            currency_regex.search(self.res.text).group(1),
            "U.S. Dollars"
        )
        self.assertEqual(
            scale_regex.search(self.res.text).group(1),
            "Millions"
        )


if __name__ == "__main__":
    unittest.main()
