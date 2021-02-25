#! python3
# functional_tests.py

import unittest

from sqv.CNBC import *
import sqv.ticker


class TestCNBCModuleErrors(unittest.TestCase):

    def test_parser_errors(self):
        # Raise sqv.CNBC.Parser.UnknownReportTypeError
        with self.assertRaises(Parser.UnknownReportTypeError):
            Parser(ticker="AAPL", report="", sheet="Balance Sheet")

        # Raise sqv.CNBC.Parser.UnknownSheetTypeError
        with self.assertRaises(Parser.UnknownSheetTypeError):
            Parser(ticker="AAPL", report="annual", sheet="")


class TestCNBCParser(unittest.TestCase):

    def test_parser(self):
        reports = ["annual", "quarter"]
        sheets = ["Balance Sheet", "Income Statement", "Cash Flow Statement"]
        for rep in reports:
            for sheet in sheets:
                parser = Parser(ticker="AAPL", report=rep, sheet=sheet)
                self.assertIsNotNone(parser.soup)

        # Create `Parser` object
        self.parser = Parser(ticker="AAPL")

        # Call `dates` classmethod
        timeperiods = self.parser.dates()
        self.assertIsInstance(timeperiods, list)
        self.assertTrue(
            all([isinstance(tp, tuple) for tp in timeperiods])
        )

        # Call `content` classmethod
        content = self.parser.content()
        self.assertIsInstance(content, dict, content)
        self.assertTrue(
            all([isinstance(v, list)
                 for v in content.values()])
        )
        self.assertTrue(
            all([isinstance(i, float) or i == '--'
                 for r in content.values()
                 for i in r]),
        )


class TestSeleniumTickerSearch(unittest.TestCase):

    def setUp(self):
        self.ticker = sqv.ticker.SeleniumTickerSearch()
        self.original_address = self.ticker.browser.current_url

    def tearDown(self):
        self.ticker.end()

    def test_selenium_ticker_search(self):
        # Invalid <country>, <security> arguments cannot be used to modify search
        with self.assertRaises(sqv.ticker.SeleniumTickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", country="Nonexistent option")
        self.ticker.reset()
        with self.assertRaises(sqv.ticker.SeleniumTickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", security="Nonexistent option")
        self.ticker.reset()

        # Search query with no results
        with self.assertRaises(sqv.ticker.SeleniumTickerSearch.ParsingError):
            self.ticker.search(name="abcdefghijklmnopqrstuvwxyz")
            self.ticker.retrieve()
        self.ticker.reset()

        # Searching with ticker results in page which cannot be parsed
        with self.assertRaises(sqv.ticker.SeleniumTickerSearch.ParsingError):
            self.ticker.search(name="AAPL")
            self.ticker.retrieve()
        self.ticker.reset()

        # Search for Apple, Inc. (AAPL)
        self.ticker.search(name="Apple", country="All", security="Stock")
        self.assertNotEqual(
            self.ticker.browser.current_url,
            self.original_address
        )

        # Retrieve table results for search query
        results = self.ticker.retrieve()
        self.assertTrue(
            results,
        )
        self.assertIn(
            "Apple Inc.",
            list(results)
        )

        # Retrieve best match for search query
        match = self.ticker.match(name="Apple Inc.")
        self.assertEqual(
            "Apple Inc.",
            match[0]
        )
        self.assertIsInstance(
            match[1], dict
        )
        self.assertEqual(
            match,
            (
                "Apple Inc.",
                {"Symbol": "AAPL", "Company": "Apple Inc.", "Exchange": "NAS"}
            )
        )


class TestTickerSearch(unittest.TestCase):

    def setUp(self):
        self.ticker = sqv.ticker.TickerSearch()

    def test_ticker_search(self):
        # Invalid <country>, <security> arguments cannot be used to modify search
        with self.assertRaises(sqv.ticker.TickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", country="Nonexistent option")
        with self.assertRaises(sqv.ticker.TickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", security="Nonexistent option")

        # Search query with no results
        with self.assertRaises(sqv.ticker.TickerSearch.ParsingError):
            self.ticker.search(name="abcdefghijklmnopqrstuvwxyz")
            self.ticker.retrieve()

        # Searching with ticker results in page which cannot be parsed
        with self.assertRaises(sqv.ticker.TickerSearch.ParsingError):
            self.ticker.search(name="AAPL")
            self.ticker.retrieve()

        # Search for Apple, Inc. (AAPL)
        self.ticker.search(name="Apple", country="All", security="Stock")

        # Retrieve table results for search query
        results = self.ticker.retrieve()
        self.assertTrue(
            results,
        )
        self.assertIn(
            "Apple Inc.",
            list(results)
        )

        # Retrieve best match for search query
        match = self.ticker.match(name="Apple Inc.")
        self.assertEqual(
            "Apple Inc.",
            match[0]
        )
        self.assertIsInstance(
            match[1], dict
        )
        self.assertEqual(
            match,
            (
                "Apple Inc.",
                {"Symbol": "AAPL", "Company": "Apple Inc.", "Exchange": "NAS"}
            )
        )


if __name__ == '__main__':
    unittest.main()
