#! python3
# tests/CNBC.py

import re
import unittest

import bs4
import requests


class TestClassParser(unittest.TestCase):

    def setUp(self):
        url = "https://apps.cnbc.com/view.asp?symbol=AAPL&uid=stocks/financials&view=incomeStatement"
        res = requests.get(url)
        self.soup = bs4.BeautifulSoup(res.text, features="lxml")

    def test_dates_css_selector(self):
        selector = "table[id='financialReportYr'] thead th"
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

    def test_labels_css_selector(self):
        selector = f"table[id='financialReportYr'] tbody tr td[class='label']"
        elems = self.soup.select(selector)
        labels = [e.getText().strip() for e in elems]
        self.assertTrue(labels)
        self.assertTrue(
            all([isinstance(t, str) for t in labels])
        )


if __name__ == "__main__":
    unittest.main()
