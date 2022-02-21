import re
import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException
from urllib.parse import urlparse

from page_loader.helpers import EMPTY_STR, get_url_without_path, HTTP, SLASH


CONNECTION_ERROR = "Some proplems with connection, resource '{}'"
HTTP_ERROR = "Some HTTP error occured, resource '{}'"
INVALID_SCHEMA = "Invalid url schema, resource '{}'"
INVALID_URL = "Invalid url, resource '{}'"
MISSING_SCHEMA = "Missing schema, resource '{}'"
NOT_STATUS_CODE_200 = "Page '{}' can't be downloaded, status code is {}"
REQUEST_EXCEPTION = "Some problems during request, resource '{}'"
STATUS_CODE_200 = 200
TOO_MANY_REDIRECTS = "Too many redirects, resource '{}'"


def get_local_resource_abs_link(link, url):
    if link.startswith(HTTP):
        return link
    else:
        url_without_path = get_url_without_path(url)
        local_resource_link = get_local_resource_relative_link(link, url)

        return url_without_path + local_resource_link


def get_local_resource_relative_link(link, url):
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
        raise ConnectionError(CONNECTION_ERROR.format(url))
    except RequestException:
        raise RequestException(REQUEST_EXCEPTION.format(url))
    else:
        if status_code != STATUS_CODE_200:
            raise HTTPError(NOT_STATUS_CODE_200.format(url, status_code))

        return response


def is_local_resource(link, url):
    link_netloc = urlparse(link).netloc
    url_netloc = urlparse(url).netloc

    return link_netloc == EMPTY_STR or link_netloc == url_netloc
