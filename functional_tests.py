#! python3
# functional_tests.py

import unittest

from sqv.CNBC import *


class TestCNBCModuleErrors(unittest.TestCase):

    def test_parser_errors(self):
        # Raise sqv.CNBC.Parser.UnknownReportTypeError
        with self.assertRaises(Parser.UnknownReportTypeError):
            Parser(ticker="AAPL", report="", sheet="Balance Sheet")

        # Raise sqv.CNBC.Parser.UnknownSheetTypeError
        with self.assertRaises(Parser.UnknownSheetTypeError):
            Parser(ticker="AAPL", report="annual", sheet="")


class TestCNBCModule(unittest.TestCase):

    def test_parser(self):
        reports = ["annual", "quarter"]
        sheets = ["Balance Sheet", "Income Statement", "Cash Flow Statement"]
        for rep in reports:
            for sheet in sheets:
                parser = Parser(ticker="AAPL", report=rep, sheet=sheet)
                self.assertIsNotNone(parser.soup)

        # Create `Parser` object
        self.parser = Parser(ticker="AAPL", report="a", sheet="bs")

        # Call `dates` classmethod
        timeperiods = self.parser.dates()
        self.assertIsInstance(timeperiods, list)
        self.assertTrue(
            all([isinstance(tp, tuple) for tp in timeperiods])
        )


if __name__ == "__main__":
    unittest.main()
