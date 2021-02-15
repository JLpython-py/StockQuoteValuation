#! python3
# functional_tests.py

import unittest

from sqv.CNBC import *


class TestCNBCModule(unittest.TestCase):

    def test_parser(self):
        # Raise sqv.CNBC.Parser.UnknownReportTypeError
        with self.assertRaises(Parser.UnknownReportTypeError):
            Parser(ticker="AAPL", report="", sheet="Balance Sheet")

        # Raise sqv.CNBC.Parser.UnknownSheetTypeError
        with self.assertRaises(Parser.UnknownSheetTypeError):
            Parser(ticker="AAPL", report="annual", sheet="")


if __name__ == "__main__":
    unittest.main()
