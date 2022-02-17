import re
import requests
from requests.exceptions import ConnectionError, RequestException

from page_loader.helpers import (
    EMPTY_STR, get_url_without_path, HTTP, KnownError, SLASH
)


CONNECTION_ERROR = "Some proplems with connection, resource '{}'"
HTTP_ERROR = "Some HTTP error occured, resource '{}'"
INVALID_SCHEMA = "Invalid url schema, resource '{}'"
INVALID_URL = "Invalid url, resource '{}'"
IO_ERROR = "Some IO error occured, resource '{}'"
MISSING_SCHEMA = "Missing schema, resource '{}'"
NOT_STATUS_CODE_200 = "Page '{}' can't be downloaded, status code is {}"
REQUEST_EXCEPTION = "Some problems during request, resource '{}'"
STATUS_CODE_200 = 200
TOO_MANY_REDIRECTS = "Too many redirects, resource '{}'"


def get_local_resource_link(link, url):
    if link.startswith(HTTP):
        url_without_path = get_url_without_path(url)
        link = re.sub(url_without_path, EMPTY_STR, link, count=1)
    elif not link.startswith(SLASH):
        link = SLASH + link
    return link.rstrip(SLASH)


def get_response_for_request(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
    except ConnectionError:
        raise KnownError(CONNECTION_ERROR.format(url))
    except RequestException:
        raise KnownError(REQUEST_EXCEPTION.format(url))
    except IOError:
        raise KnownError(IO_ERROR.format(url))
    else:
        if status_code != STATUS_CODE_200:
            raise KnownError(NOT_STATUS_CODE_200.format(url, status_code))

        return response
