#! python3
# ticker_tests.py

import json
import os
import unittest

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


class TestFindElementsOnPage(unittest.TestCase):

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

    def test_find_all_elements(self):
        self.assertEqual(
            self.browser.title,
            "Stock Ticker Symbol Lookup - MarketWatch"
        )
        for sel in self.fields:
            self.assertEqual(
                len(self.browser.find_elements_by_css_selector(self.fields[sel])),
                1,
                sel
            )
        for sel in self.options:
            self.assertTrue(
                self.browser.find_elements_by_css_selector(self.options[sel]),
                sel
            )


if __name__ == '__main__':
    unittest.main()
