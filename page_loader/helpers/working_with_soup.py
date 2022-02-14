import logging
import os
from urllib.parse import urlparse

from page_loader.helpers import EMPTY_STR, SLASH
from page_loader.helpers.working_with_fs import (
    download_local_resource, get_loaded_local_resource_file_path
)
from page_loader.helpers.working_with_requests import get_local_resource_link


CHANGED_RESOURCE_LINK = "Resource link was changed from '{}' to '{}'"
HREF = 'href'
IMG = 'img'
LINK = 'link'
RECEIVED_LOADED_RESOURCE_PATH = (
    "Loaded resource path from page '{}' was received"
)
RECEIVED_LOCAL_RESOURCE_LINK = (
    "Local resource link from page '{}' was received"
)
SCRIPT = 'script'
SRC = 'src'
TAGS_LINK_ATTRS = {
    IMG: SRC,
    LINK: HREF,
    SCRIPT: SRC
}


def get_updated_soup(soup, url, output_path):
    for tag, link_attr in TAGS_LINK_ATTRS.items():
        for tag in soup.find_all(tag):
            tag_attr_link = tag.get(link_attr)

            if not is_local_resource(tag_attr_link, url):
                continue

            local_resource_link = get_local_resource_link(tag_attr_link, url)
            local_resource_abs_link = url.rstrip(SLASH) + local_resource_link
            logging.info(
                RECEIVED_LOCAL_RESOURCE_LINK.format(local_resource_abs_link)
            )

            loaded_resource_path = get_loaded_local_resource_file_path(
                local_resource_link,
                url
            )
            logging.info(
                RECEIVED_LOADED_RESOURCE_PATH.format(local_resource_abs_link)
            )

            tag[link_attr] = loaded_resource_path
            logging.info(
                CHANGED_RESOURCE_LINK.format(
                    local_resource_link,
                    loaded_resource_path
                )
            )

            download_local_resource(
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
