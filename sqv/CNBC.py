#! python3
# sqv.CNBC

"""

"""

import logging

import openpyxl

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s"
)


class Parser:
    """ Parse financial sheet webpages for financial sheet data
"""
    def __init__(self, *, report):
        report = report.lower()
        if report not in ["annual", "quarter"]:
            raise self.UnknownReportTypeError(report)
        self.report = report

    class UnknownReportTypeError(Exception):

        def __init__(self, report):
            self.report = report
            self.message = f"No financial sheet '{self.report}'"
            super().__init__(self.message)
