import jsonpickle
import unirest

from seatsio.exceptions import SeatsioException


class HttpClient:

    def __init__(self, base_url, secret_key):
        self.baseUrl = base_url
        self.secretKey = secret_key

    def get(self, url):
        return GET(self.__create_full_url(url)).auth(self.secretKey, '').execute()

    def post(self, url, body=None):
        return POST(self.__create_full_url(url)).auth(self.secretKey, '').body(body).execute()

    def __create_full_url(self, relative_url):
        return self.baseUrl + relative_url


class HttpRequest:
    def __init__(self, method, full_url):
        self.httpMethod = method
        self.url = full_url

    def auth(self, username, password):
        self.credentials = (username, password)
        return self

    def execute(self):
        response = self.try_execute()
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response

    def try_execute(self):
        raise NotImplementedError


class GET(HttpRequest):

    def __init__(self, url):
        HttpRequest.__init__(self, "GET", url)

    def auth(self, username, password):
        self.credentials = (username, password)
        return self

    def try_execute(self):
        try:
            return unirest.get(self.url, auth=self.credentials)
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class POST(HttpRequest):

    def __init__(self, url):
        HttpRequest.__init__(self, "POST", url)
        self.bodyObject = None

    def body(self, body):
        self.bodyObject = body
        return self

    def try_execute(self):
        try:
            if self.bodyObject:
                json = jsonpickle.encode(self.bodyObject, unpicklable=False)
                return unirest.post(
                    url=self.url,
                    auth=self.credentials,
                    headers={"Accept": "application/json"},
                    params=json
                )
            else:
                return unirest.post(
                    url=self.url,
                    auth=self.credentials
                )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)
