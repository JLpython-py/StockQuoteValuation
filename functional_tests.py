#! python3
# functional_tests.py

import unittest

from sqv import CNBC
from sqv import ticker
from sqv import YahooFinance


class TestCNBCModuleErrors(unittest.TestCase):

    def test_parser_errors(self):
        # Raise CNBC.Parser.UnknownReportTypeError
        with self.assertRaises(CNBC.Parser.UnknownReportTypeError):
            CNBC.Parser("AAPL", report="", sheet="Balance Sheet")

        # Raise CNBC.Parser.UnknownSheetTypeError
        with self.assertRaises(CNBC.Parser.UnknownSheetTypeError):
            CNBC.Parser("AAPL", report="annual", sheet="")


class TestYahooFinanceModuleErrors(unittest.TestCase):

    def test_parser_errors(self):
        # Raise YahooFinance.Parser.UnknownReportTypeError
        with self.assertRaises(YahooFinance.Parser.UnknownReportTypeError):
            YahooFinance.Parser("AAPL", report="", sheet="Balance Sheet")

        # Raise YahooFinance.Parser.UnknownSheetTypeError
        with self.assertRaises(YahooFinance.Parser.UnknownSheetTypeError):
            YahooFinance.Parser("AAPL", report="annual", sheet="")


class TestCNBCParser(unittest.TestCase):

    def test_parser(self):
        reports = ["annual", "quarter"]
        sheets = ["Balance Sheet", "Income Statement", "Cash Flow Statement"]
        for rep in reports:
            for sheet in sheets:
                parser = CNBC.Parser("AAPL", report=rep, sheet=sheet)
                self.assertIsNotNone(parser.soup)

        # Create `Parser` object
        self.parser = CNBC.Parser("AAPL")

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


class TestYahooFinanceParser(unittest.TestCase):

    def test_parser(self):
        reports = ["annual", "quarter"]
        sheets = ["Balance Sheet", "Income Statement", "Cash Flow Statement"]
        for rep in reports:
            for sheet in sheets:
                parser = YahooFinance.Parser("AAPL", report=rep, sheet=sheet)
                self.assertIsNotNone(parser.tree)

        # Create `Parser` object
        self.parser = YahooFinance.Parser("AAPL")

        # Call `dates` classmethod
        timeperiods = self.parser.dates()
        self.assertIsInstance(timeperiods, list)
        self.assertTrue(
            all([isinstance(tp, str) for tp in timeperiods])
        )


class TestSeleniumTickerSearch(unittest.TestCase):

    def setUp(self):
        self.ticker = ticker.SeleniumTickerSearch()
        self.original_address = self.ticker.browser.current_url

    def tearDown(self):
        self.ticker.end()

    def test_selenium_ticker_search(self):
        # Invalid <country>, <security> arguments cannot be used to modify search
        with self.assertRaises(ticker.SeleniumTickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", country="Nonexistent option")
        self.ticker.reset()
        with self.assertRaises(ticker.SeleniumTickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", security="Nonexistent option")
        self.ticker.reset()

        # Search query with no results
        with self.assertRaises(ticker.SeleniumTickerSearch.ParsingError):
            self.ticker.search(name="abcdefghijklmnopqrstuvwxyz")
            self.ticker.retrieve()
        self.ticker.reset()

        # Searching with ticker results in page which cannot be parsed
        with self.assertRaises(ticker.SeleniumTickerSearch.ParsingError):
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
        self.ticker = ticker.TickerSearch()

    def test_ticker_search(self):
        # Invalid <country>, <security> arguments cannot be used to modify search
        with self.assertRaises(ticker.TickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", country="Nonexistent option")
        with self.assertRaises(ticker.TickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", security="Nonexistent option")

        # Search query with no results
        with self.assertRaises(ticker.TickerSearch.ParsingError):
            self.ticker.search(name="abcdefghijklmnopqrstuvwxyz")
            self.ticker.retrieve()

        # Searching with ticker results in page which cannot be parsed
        with self.assertRaises(ticker.TickerSearch.ParsingError):
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
