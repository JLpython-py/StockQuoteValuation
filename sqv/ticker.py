#! python3
# ticker.py

import json
import logging

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s"
)


class TickerSearch:

    def __init__(self):
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

    def search(self, *, name, country="United States", security_type="All"):
        pass
