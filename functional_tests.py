#! python3
# functional_tests.py

import unittest

import sqv.ticker


class TestSQVTicker(unittest.TestCase):

    def setUp(self):
        self.ticker = sqv.ticker.TickerSearch()
        self.original_address = self.ticker.browser.current_url

    def tearDown(self):
        self.ticker.end()

    def test_ticker_module(self):
        # Invalid <country>, <security> arguments cannot be used to modify search
        with self.assertRaises(sqv.ticker.TickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", country="Nonexistent option")
        self.ticker.reset()
        with self.assertRaises(sqv.ticker.TickerSearch.OptionNotFoundError):
            self.ticker.search(name="Apple", security="Nonexistent option")
        self.ticker.reset()

        # Searching with ticker results in page which cannot be parsed
        with self.assertRaises(sqv.ticker.TickerSearch.ParsingError):
            self.ticker.search(name="AAPL")
            self.ticker.retrieve()
        self.ticker.reset()

        # Search for Apple, Inc. (AAPL)
        self.ticker.search(name="Apple", country="All", security="Stock")
        self.assertNotEqual(
            self.ticker.browser.current_url,
            self.original_address
        )

        # Retrieve table results
        results = self.ticker.retrieve()
        self.assertTrue(
            results,
        )
        self.assertIn(
            "Apple, Inc.",
            results
        )


if __name__ == '__main__':
    unittest.main()
