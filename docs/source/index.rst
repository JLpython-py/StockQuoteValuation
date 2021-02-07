.. StockQuoteValuation documentation master file, created by
   sphinx-quickstart on Sat Feb  6 15:00:30 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

###############################################################################
StockQuoteValuation Documentation
###############################################################################

.. toctree::
   :maxdepth: 2
   :caption: Contents:

SQV is an open-source project. 

See this project's `GitHub Repository`_ or the `latest releases`_.

.. _GitHub Repository: https://github.com/JLpython-py/StockQuoteValuation
.. _latest releases: https://github.com/JLpython-py/StockQuoteValuation/releases

*******************************************************************************
SQV.ticker
*******************************************************************************

.. py:class:: class sqv.ticker.TickerSearch

   .. py:classmethod:: TickerSearch.__init__(self)

      .. py:attribute:: fields

         :type: dict

         A dictionary mapping the webpage search query fields to the corresponding CSS selector

      .. py:attribute:: options

         :type: dict

         A dictionary mapping the webpage search query field options to the corresponding CSS selector

      .. py:attribute:: browser

         :type: `selenium.webdriver.firefox.webdriver.WebDriver`_

         A Selenium Firefox browser used to navigate the webpage at ``address``

      .. py:attribute:: address

         :type: str

         The address to the `MarketWatch Ticker Lookup tool`_

   .. py:exception:: sqv.ticker.TickerSearch.OptionNotFoundError(Exception, field, option, options)

      :param str field: The search query field which the user attempted to modify
      :param str option: The option which the user tried to set the ``field`` argument to
      :param list options: A list of options (titlecase) to which the ``field`` argument can be set to

      Raised when a search query field cannot be set to the passed option

   .. py:exception:: sqv.ticker.TickerSearch.ParsingError(Exception)

      Raised when a resulting search query page cannot be parsed for the contained data.
      There are two common scenarios in which this error is raised:

      #. The ``name`` argument passed is a valid ticker, causing the page to redirect to the stock quote
      #. The search criteria result in no results.

   .. py:classmethod:: end(self)

      Calls the ``quit`` classmethod of :py:attr:browser

   .. py:classmethod:: reset(self)

      Calls the ``get`` classmethod of :py:attr:browser, passing :py:attr:address

   .. py:classmethod:: search(self, *, name, country="United States", security="All")

      :param str name: The search term
      :param str country: The country of the security
      :param str security: The type of security
      :raises sqv.ticker.TickerSearch.OptionNotFoundError: If either the **country** or **security** field cannot be set to the value passed to the respective ``country`` and/or ``security`` parameters

      Fills out the search query fields on the webpage
      The arguments passed are entered into the corresponding fields by :py:attr:`browser`, then the **SEARCH** button is clicked

   .. py:classmethod:: retrieve(self, *, limit=None)

      :param int limit: The maximum length of the returned dictionary, or, when ``None``, all results will be returned
      :return: A dictionary of nested dictionaries containing the data in the table returned by the search query
      :rtype: dict
      :raises sqv.ticker.TickerSearch.ParsingError: If the webpage resulting from the search query cannot be parsed for ticker data

      Parses the current page to extract the data contained in the table returned by the search query
      Data is ordered in the dictionary A-Z-a-z

   .. py:classmethod:: match(self, *, name)

      :param str name: The search term
      :return: The name of the best match and the corresponding dictionary of the best match
      :rtype: tuple

      Calls :py:meth:`retrieve` for a dictionary of possible matches (``results``).
      Calls the ``extractOne`` function of the `fuzzywuzzy.process`_, passing ``name`` (titlecase) and ``list(results)``.

.. _selenium.webdriver.firefox.webdriver.WebDriver: https://selenium-python.readthedocs.io/api.html#webdriver-api
.. _MarketWatch Ticker Lookup tool: https://www.marketwatch.com/tools/quotes/lookup.asp
.. _fuzzywuzzy.process: https://pypi.org/project/fuzzywuzzy/


###############################################################################
Indices and tables
###############################################################################


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
