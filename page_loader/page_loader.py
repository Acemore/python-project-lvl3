import os
import re
import requests
from urllib.parse import urlparse


DOT = '.'
EMPTY_STR = ''
HTML_EXT = '.html'
HYPHEN = '-'
NOT_LETTER_AND_NOT_DIGIT_REGEXP = r'[^a-zA-Z0-9]'
SCHEME_END = '://'
SLASH = '/'


def get_loaded_file_full_path(url, output_path):
    if output_path.startswith(DOT):
        output_path = re.sub(DOT, os.getcwd(), output_path, count=1)

    scheme = urlparse(url).scheme + SCHEME_END
    url_without_scheme = re.sub(scheme, EMPTY_STR, url, count=1)
    if url_without_scheme.endswith(SLASH):
        url_without_scheme = url_without_scheme[:-1]
    loaded_file_name_without_ext = re.sub(
        NOT_LETTER_AND_NOT_DIGIT_REGEXP,
        HYPHEN,
        url_without_scheme
    )
    loaded_file_name = loaded_file_name_without_ext + HTML_EXT

    return os.path.join(output_path, loaded_file_name)


def download(url, output_path=os.getcwd()):
    loaded_file_full_path = get_loaded_file_full_path(url, output_path)
    response = requests.get(url)

    with open(loaded_file_full_path, 'w') as loaded_file:
        loaded_file.write(response.text)
    return loaded_file_full_path
