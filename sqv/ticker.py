#! python3
# ticker.py

"""
==============================================================================
MIT License

Copyright (c) 2021 Jacob Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import urllib.request

from fuzzywuzzy import process
from lxml import etree
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


COUNTRY = {
    "United States": "us",
    "All": "all",
    "Canada": "ca",
    "France": "fr",
    "Germany": "de",
    "Hong Kong": "hk",
    "Italy": "it",
    "Japan": "jp",
    "Netherlands": "nl",
    "New Zealand": "nz",
    "Norway": "no",
    "South Africa": "za",
    "Spain": "es",
    "Sweden": "se",
    "Switzerland": "ch",
    "United Kingdom": "uk"
}
SECURITY = {
    "All": "All",
    "Stock": "Stock",
    "Fund": "Fund",
    "Index": "Index",
    "Currency": "Currency"
}


class TickerSearch:

    def __init__(self):
        self.base = "https://www.marketwatch.com/tools/quotes/lookup.asp?siteID=mktw&Lookup={}&Country={}&Type={}"
        self.address = ""

    class OptionNotFoundError(Exception):
        """ Raised for errors in TickerSearch.search while searching for ticker

        Attributes:
            field -- The field which user attempted to modify
            option -- The option which the user attempted to set the field to
"""

        def __init__(self, field, option, options):
            self.field = field
            self.option = option
            self.message = f"Could not find '{self.option}' for '{self.field}'"
            super().__init__(f"{self.message} ({options})")

    class ParsingError(Exception):
        """ Raised for errors in TickerSearch.retrieve when scraping table
"""

        def __init__(self):
            self.message = "Resulting page cannot be parsed."
            super().__init__(self.message)

    def search(self, *, name, country="United States", security="All"):
        country, security = country.title(), security.title()
        if country not in COUNTRY:
            raise self.OptionNotFoundError(
                "country", country,
                list(COUNTRY)
            )
        if security not in SECURITY:
            raise self.OptionNotFoundError(
                "security", security,
                list(SECURITY)
            )
        name = '+'.join(name.split(' '))
        self.address = self.base.format(
            name, COUNTRY[country], SECURITY[security]
        )
        res = urllib.request.urlopen(self.address)
        if res.getcode() != 200:
            raise self.ParsingError()

    def retrieve(self, limit=None):
        """ Return data contained in table returned by search (Order: A-Za-z)

        Arguments:
              limit -- The maximum number of items returned
"""
        results = {}
        # Create XPath parser for current URL
        response = urllib.request.urlopen(self.address)
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
        raw_headings = tree.xpath(
            "/html/body/div[1]/div[3]/div[2]/div[1]/div/table/thead/tr"
        )
        if len(raw_headings) == 0:
            raise self.ParsingError()
        headings = [c.text for c in raw_headings[0].getchildren()]
        raw_rows = tree.xpath(
            "/html/body/div[1]/div[3]/div[2]/div[1]/div/table/tbody/tr"
        )
        if limit is not None:
            splice = raw_rows[:limit]
        else:
            splice = raw_rows[:]
        for row in splice:
            items = []
            for des in row.iterdescendants():
                if des.text is None:
                    continue
                items.append(des.text)
            data = dict(zip(headings, items))
            results.setdefault(
                data["Company"], data
            )
        return results

    def match(self, *, name):
        """ Returns the result which best matches the <name> argument
"""
        results = self.retrieve()
        res = process.extractOne(
            name.title(), list(results.keys())
        )
        return res[0], results[res[0]]


class SeleniumTickerSearch:
    """ Searches for ticker symbol with MarketWatch Stock Ticker Symbol Lookup feature
"""
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
        self.address = "https://www.marketwatch.com/tools/quotes/lookup.asp"
        self.browser.get(self.address)
        self.etree = None

    class OptionNotFoundError(Exception):
        """ Raised for errors in TickerSearch.search while searching for ticker

        Attributes:
            field -- The field which user attempted to modify
            option -- The option which the user attempted to set the field to
"""
        def __init__(self, field, option, options):
            self.field = field
            self.option = option
            self.message = f"Could not find '{self.option}' for '{self.field}'"
            super().__init__(f"{self.message} ({options})")

    class ParsingError(Exception):
        """ Raised for errors in TickerSearch.retrieve when scraping table
"""
        def __init__(self):
            self.message = "Resulting page cannot be parsed."
            super().__init__(self.message)

    def end(self):
        """ Call `quit` method of `self.browser`
"""
        self.browser.quit()

    def reset(self):
        """ Navigate browser to original page
"""
        self.browser.get(self.address)

    def search(self, *, name, country="United States", security="All"):
        """ Fill out Symbol Lookup search query
"""
        country, security = country.title(), security.title()
        # Enter <name> argument into name input box
        self.browser.find_element_by_css_selector(
            self.fields.get('name')
        ).send_keys(name)
        # Open country select menu
        self.browser.find_element_by_css_selector(
            self.fields.get('country')
        ).click()
        # Get element corresponding to <country> argument, if exists, and click
        country_options = self.browser.find_elements_by_css_selector(
            self.options.get('country')
        )
        country_opt = None
        for elem in country_options:
            if elem.text == country:
                country_opt = elem
        if country_opt is None:
            raise self.OptionNotFoundError(
                "country", country,
                [e.text.title() for e in country_options]
            )
        country_opt.click()
        # Get element corresponding to <security> argument, if exists, and click
        self.browser.find_element_by_css_selector(
            self.fields.get('security')
        ).click()
        security_options = self.browser.find_elements_by_css_selector(
            self.options.get('security')
        )
        security_opt = None
        for elem in security_options:
            if elem.text == security:
                security_opt = elem
        if security_opt is None:
            raise self.OptionNotFoundError(
                "security", security,
                [e.text.title() for e in security_options]
            )
        security_opt.click()
        # Click search button to submit query
        self.browser.find_element_by_css_selector(
            self.fields.get('search')
        ).click()

    def retrieve(self, limit=None):
        """ Return data contained in table returned by search (Order: A-Za-z)

        Arguments:
              limit -- The maximum number of items returned
"""
        if self.browser.title != "Stock Ticker Symbol Lookup - MarketWatch":
            raise self.ParsingError()
        results = {}
        # Create XPath parser for current URL
        response = urllib.request.urlopen(self.browser.current_url)
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
        raw_headings = tree.xpath(
            "/html/body/div[1]/div[3]/div[2]/div[1]/div/table/thead/tr"
        )
        if len(raw_headings) == 0:
            raise self.ParsingError()
        headings = [c.text for c in raw_headings[0].getchildren()]
        raw_rows = tree.xpath(
            "/html/body/div[1]/div[3]/div[2]/div[1]/div/table/tbody/tr"
        )
        if limit is not None:
            splice = raw_rows[:limit]
        else:
            splice = raw_rows[:]
        for row in splice:
            items = []
            for des in row.iterdescendants():
                if des.text is None:
                    continue
                items.append(des.text)
            data = dict(zip(headings, items))
            results.setdefault(
                data["Company"], data
            )
        return results

    def match(self, *, name):
        """ Returns the result which best matches the <name> argument
"""
        results = self.retrieve()
        res = process.extractOne(
            name.title(), list(results.keys())
        )
        return res[0], results[res[0]]
