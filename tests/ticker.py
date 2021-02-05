#! python3
# ticker_tests.py

import json
import unittest
import urllib.request

from lxml import etree
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class TestCSSSelectorsFile(unittest.TestCase):

    def setUp(self):
        with open("data/ticker/fields.txt") as file:
            self.fields = json.load(file)
        with open("data/ticker/options.txt") as file:
            self.options = json.load(file)

    def test_fields_file_format(self):
        self.assertIsInstance(
            self.fields, dict
        )
        self.assertTrue(
            all([isinstance(k, str) for k in self.fields])
        )
        self.assertEqual(
            set(list(self.fields)),
            {"name", "country", "security", "search"}
        )
        self.assertTrue(
            all([isinstance(self.fields[k], str) for k in self.fields])
        )

    def test_options_file_format(self):
        self.assertIsInstance(
            self.options, dict
        )
        self.assertTrue(
            all([isinstance(k, str) for k in self.options])
        )
        self.assertEqual(
            set(list(self.options)),
            {"country", "security"}
        )
        self.assertTrue(
            all([isinstance(self.options[k], str) for k in self.options])
        )


class TestSearch(unittest.TestCase):

    def setUp(self):
        with open("data/ticker/fields.txt") as file:
            self.fields = json.load(file)
        with open("data/ticker/options.txt") as file:
            self.options = json.load(file)
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(
            options=options
        )
        address = "https://www.marketwatch.com/tools/quotes/lookup.asp"
        self.browser.get(address)

    def tearDown(self):
        self.browser.quit()

    def test_correct_address(self):
        self.assertEqual(
            self.browser.title,
            "Stock Ticker Symbol Lookup - MarketWatch"
        )

    def test_field_css_selectors(self):
        for sel in self.fields:
            self.assertEqual(
                len(self.browser.find_elements_by_css_selector(self.fields[sel])),
                1,
                sel
            )

    def test_options_css_selector(self):
        for sel in self.options:
            self.assertTrue(
                self.browser.find_elements_by_css_selector(self.options[sel]),
                sel
            )


class TestRetrieve(unittest.TestCase):

    def setUp(self):
        response = urllib.request.urlopen(
            "https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup=apple&Country=us&Type=All"
        )
        htmlparser = etree.HTMLParser()
        self.tree = etree.parse(response, htmlparser)

    def test_headings_xpath(self):
        raw_headings = self.tree.xpath(
            "/html/body/div[1]/div[3]/div[2]/div[1]/div/table/thead/tr"
        )
        self.assertEqual(
            len(raw_headings),
            1
        )
        self.assertEqual(
            len(raw_headings[0].getchildren()),
            3
        )
        self.assertEqual(
            set([c.text for c in raw_headings[0].getchildren()]),
            {"Symbol", "Company", "Exchange"}
        )

    def test_rows_xpath(self):
        raw_rows = self.tree.xpath(
            "/html/body/div[1]/div[3]/div[2]/div[1]/div/table/tbody/tr"
        )
        self.assertTrue(
            raw_rows
        )
        self.assertEqual(
            len(list(raw_rows[0].iterdescendants())),
            4
        )
        self.assertEqual(
            len([des.text for des in raw_rows[0].iterdescendants()
             if des.text is not None]),
            3
        )


if __name__ == '__main__':
    unittest.main()
