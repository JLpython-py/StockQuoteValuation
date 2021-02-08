###############################################################################
sqv.ticker.TickerSearch
###############################################################################

.. py:class:: class sqv.ticker.TickerSearch

   .. py:classmethod:: __init__(self)

      .. py:attribute:: base

         :type: str

         The template for the address to the `MarketWatch Ticker Lookup tool`_

      .. py:attribute:: address

         :type: str

         The address to the specific search

   .. py:exception:: sqv.ticker.TickerSearch.OptionNotFoundError(Exception, field, option, options)

      :param str field: The search query field which the user attempted to modify
      :param str option: The option which the user tried to set the ``field`` argument to
      :param list options: A list of options (titlecase) to which the ``field`` argument can be set to

      Raised when a search query field cannot be set to the passed option.

   .. py:exception:: sqv.ticker.TickerSearch.ParsingError(Exception)

      Raised when a resulting search query page cannot be parsed for the contained data.
      There are two common scenarios in which this error is raised:

      #. The ``name`` argument passed is a valid ticker, causing the page to redirect to the stock quote
      #. The search criteria result in no results.

   .. py:classmethod:: search(self, *, name, country="United States", security="All")

      :param str name: The search term
      :param str country: The country of the security
      :param str security: The type of security
      :raises sqv.ticker.TickerSearch.OptionNotFoundError: If ``urllib.request.urlopen(self.address).getcode()`` does not equal 200

      The address of :py:attr:`base` is formatted according to the arguments passed and stored in :py:attr:`address`.
      The placeholders are replaced, in order, with the following values:

      #. ``'+'.join(name.split(' '))``
      #. the value in :py:data:`COUNTRY` with corresponds to ``country``
      #. the value in :py:data:`SECURITY` with corresponds to ``security``

      The status code of the return value of passing :py:attr:`address` to ``urllib.request.urlopen`` is checked to verify search.

   .. py:classmethod:: retrieve(self, *, limit=None)

      :param int limit: The maximum length of the returned dictionary, or, when ``None``, all results will be returned
      :return: A dictionary of nested dictionaries containing the data in the table returned by the search query
      :rtype: dict
      :raises sqv.ticker.TickerSearch.ParsingError: If the webpage resulting from the search query cannot be parsed for ticker data

      Parses the current page to extract the data contained in the table returned by the search query.
      Data is ordered in the dictionary A-Z-a-z.

   .. py:classmethod:: match(self, *, name)

      :param str name: The search term
      :return: The name of the best match and the corresponding dictionary of the best match
      :rtype: tuple

      Calls :py:meth:`retrieve` for a dictionary of possible matches (``results``).
      Calls the ``extractOne`` function of the `fuzzywuzzy.process`_, passing ``name`` (titlecase) and ``list(results)``.


.. _MarketWatch Ticker Lookup tool: https://www.marketwatch.com/tools/quotes/lookup.asp
.. _fuzzywuzzy.process: https://pypi.org/project/fuzzywuzzy/
