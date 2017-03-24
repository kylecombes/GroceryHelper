class SupermarketAPIBase:

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    URL_BASE = 'http://www.SupermarketAPI.com/api.asmx/'
    API_KEY_URL_PARAM = 'APIKEY'

    def __init__(self, api_key):
        self.api_key = api_key

    def build_url(self, request_type, **params):
        """ Builds a request URL

            :param request_type: the API call to use (e.g. 'SearchForItem') - string
            :param params: the parameters to include in the request - <string,string>
            :returns the full URL for the request as a string - string
        """
        url = '%s%s?%s=%s' % (self.URL_BASE, request_type, self.API_KEY_URL_PARAM, self.api_key)
        for param, val in params.items():
            url = '%s&%s=%s' % (url, param, val)

        return url
