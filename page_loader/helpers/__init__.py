import re
from urllib.parse import urlparse


EMPTY_STR = ''
HTTP = 'http'
SLASH = '/'


class KnownError(Exception):
    pass


def get_url_without_path(url):
    path = urlparse(url).path
    return url.rstrip(path) if path == SLASH else re.sub(
        path, EMPTY_STR, url, count=1
    )
