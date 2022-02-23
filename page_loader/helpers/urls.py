import os
import re
from urllib.parse import urlparse

from page_loader.helpers import EMPTY_STR, get_url_without_path, HTTP, SLASH


DOT = '.'
EXT_REGEXP = r'\.[^.\/]+$'
FILES_POSTFIX = '_files'
HTML_EXT = '.html'
HYPHEN = '-'
NOT_LETTER_AND_NOT_DIGIT_REGEXP = r'[^a-zA-Z0-9]'
QUERY_STRING = r'\?[^?]+$'
SCHEME_END = '://'


def get_hyphenated_str(str):
    return re.sub(
        NOT_LETTER_AND_NOT_DIGIT_REGEXP,
        HYPHEN,
        str
    )


def get_loaded_local_resource_file_name(local_resource_link, url):
    netloc = urlparse(url).netloc
    hyphenated_netloc = get_hyphenated_str(netloc)

    local_resource_link = re.sub(
        QUERY_STRING,
        EMPTY_STR,
        local_resource_link,
        count=1
    )
    local_resource_link_without_ext, ext = os.path.splitext(local_resource_link)
    if not ext:
        ext = HTML_EXT

    hyphenated_local_resource_link_without_ext = (
        get_hyphenated_str(local_resource_link_without_ext)
    )

    return '{}{}{}'.format(
        hyphenated_netloc,
        hyphenated_local_resource_link_without_ext,
        ext
    )


def get_loaded_local_resource_file_path(local_resource_link, url):
    return os.path.join(
        get_loaded_local_resources_dir_name(url),
        get_loaded_local_resource_file_name(local_resource_link, url)
    )


def get_loaded_local_resources_dir_name(url):
    loaded_main_page_name = get_loaded_main_page_file_name(url)

    return re.sub(EXT_REGEXP, EMPTY_STR, loaded_main_page_name) + FILES_POSTFIX


def get_loaded_main_page_file_full_path(url, output_path):
    if output_path.startswith(DOT):
        output_path = re.sub(DOT, os.getcwd(), output_path, count=1)

    loaded_main_page_name = get_loaded_main_page_file_name(url)

    return os.path.join(output_path, loaded_main_page_name)


def get_loaded_main_page_file_name(url):
    scheme = urlparse(url).scheme + SCHEME_END
    url_without_scheme = re.sub(scheme, EMPTY_STR, url, count=1)

    if url_without_scheme.endswith(SLASH):
        url_without_scheme = url_without_scheme.rstrip(SLASH)

    url_path_ext = HTML_EXT
    if url_path := urlparse(url).path:
        _, ext = os.path.splitext(url_path)
        if ext:
            url_path_ext = ext

    url_without_scheme_and_ext = (
        re.sub(EXT_REGEXP, EMPTY_STR, url_without_scheme)
    )
    hyphenated_url_without_scheme = (
        get_hyphenated_str(url_without_scheme_and_ext)
    )
    return hyphenated_url_without_scheme + url_path_ext


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


def is_local_resource(link, url):
    link_netloc = urlparse(link).netloc
    url_netloc = urlparse(url).netloc

    return link_netloc == EMPTY_STR or link_netloc == url_netloc
