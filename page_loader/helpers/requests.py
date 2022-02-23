import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException


CONNECTION_ERROR = "Some proplems with connection, resource '{}'"
HTTP_ERROR = "Some HTTP error occured, resource '{}'"
INVALID_SCHEMA = "Invalid url schema, resource '{}'"
INVALID_URL = "Invalid url, resource '{}'"
MISSING_SCHEMA = "Missing schema, resource '{}'"
NOT_STATUS_CODE_200 = "Page '{}' can't be downloaded, status code is {}"
REQUEST_EXCEPTION = "Some problems during request, resource '{}'"
STATUS_CODE_200 = 200
TOO_MANY_REDIRECTS = "Too many redirects, resource '{}'"


def get_response_for_request(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
    except ConnectionError:
        raise ConnectionError(CONNECTION_ERROR.format(url))
    except RequestException:
        raise RequestException(REQUEST_EXCEPTION.format(url))
    else:
        if status_code != STATUS_CODE_200:
            raise HTTPError(NOT_STATUS_CODE_200.format(url, status_code))

        return response
