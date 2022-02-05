import os
import re
import requests
from urllib.parse import urlparse

from page_loader.hyphenated_str_getter import (
    EMPTY_STR,
    get_hyphenated_name,
    get_hyphenated_str,
    SLASH
)


FILES_POSTFIX = '_files'
HREF = 'href'
HTML_EXT = '.html'
HTTP = 'http'
IMG = 'img'
LINK = 'link'
QUERY_STRING = r'\?[^?]+$'
SCRIPT = 'script'
SRC = 'src'
TAGS_LINK_ATTRS = {
    IMG: SRC,
    LINK: HREF,
    SCRIPT: SRC
}


def download_resource(url, output_path):
    response = requests.get(url)
    response_chunks = response.iter_content()

    with open(output_path, 'wb') as loaded_file:
        for response_chunk in response_chunks:
            loaded_file.write(response_chunk)


def get_loaded_resource_name(local_resource_link, url):
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


def get_loaded_resource_path(local_resource_link, url):
    return os.path.join(
        get_hyphenated_name(url, FILES_POSTFIX),
        get_loaded_resource_name(local_resource_link, url)
    )


def get_local_resource_link(link, url):
    if link.startswith(HTTP):
        link = re.sub(url, EMPTY_STR, link, count=1)
    elif not link.startswith(SLASH):
        link = SLASH + link
    return link.rstrip(SLASH)


def get_updated_soup(soup, url, output_path):
    for tag, link_attr in TAGS_LINK_ATTRS.items():
        for tag in soup.find_all(tag):
            tag_attr_link = tag.get(link_attr)

            if not is_local_resource(tag_attr_link, url):
                continue

            local_resource_link = get_local_resource_link(tag_attr_link, url)
            loaded_resource_path = get_loaded_resource_path(
                local_resource_link,
                url
            )

            tag[link_attr] = loaded_resource_path

            download_resource(
                url + local_resource_link,
                os.path.join(
                    output_path,
                    loaded_resource_path
                )
            )

    return soup.prettify()


def is_local_resource(link, url):
    link_netloc = urlparse(link).netloc
    url_netloc = urlparse(url).netloc

    return link_netloc == EMPTY_STR or link_netloc == url_netloc
