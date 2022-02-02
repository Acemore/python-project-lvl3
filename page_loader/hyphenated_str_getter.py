import re
from urllib.parse import urlparse


EMPTY_STR = ''
HYPHEN = '-'
NOT_LETTER_AND_NOT_DIGIT_REGEXP = r'[^a-zA-Z0-9]'
SCHEME_END = '://'
SLASH = '/'


def get_hyphenated_str(str):
    return re.sub(
        NOT_LETTER_AND_NOT_DIGIT_REGEXP,
        HYPHEN,
        str
    )


def get_hyphenated_name(url, postfix):
    scheme = urlparse(url).scheme + SCHEME_END
    url_without_scheme = re.sub(scheme, EMPTY_STR, url, count=1)
    if url_without_scheme.endswith(SLASH):
        url_without_scheme = url_without_scheme[:-1]
    hyphenated_url_without_scheme = get_hyphenated_str(url_without_scheme)

    return hyphenated_url_without_scheme + postfix
