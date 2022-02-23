import os
from bs4 import BeautifulSoup
from progress.bar import Bar

from page_loader.helpers.io import (
    create_loaded_local_resources_dir, write_loaded_local_resource,
    write_loaded_main_page
)
from page_loader.helpers.requests import get_response_for_request
from page_loader.helpers.urls import (
    get_loaded_local_resources_dir_name, get_loaded_local_resource_file_path,
    get_loaded_main_page_file_full_path, get_local_resource_abs_link,
    get_local_resource_relative_link, is_local_resource

)
from page_loader.logger import get_logger


CHANGED_RESOURCE_LINK = "Resource link was changed from '{}' to '{}'"
CREATED_LOADED_PAGE_SOUP = 'Loaded page soup was received'
HREF = 'href'
IMG = 'img'
LINK = 'link'
LOADED_ALL_RESOURCES = 'All local resources were downloaded'
LOADED_RESOURCE = "Resource from page '{}' was loaded to path '{}'"
RECEIVED_ORIGINAL_HTML = 'Original html was received'
RECEIVED_LOADED_PAGE_FULL_PATH = 'Loaded page full path was received'
RECEIVED_LOADED_RESOURCE_PATH = (
    "Loaded resource path from page '{}' was received"
)
RECEIVED_LOCAL_RESOURCE_LINK = (
    "Local resource link from page '{}' was received"
)
SCRIPT = 'script'
SRC = 'src'
UPDATED_LOADED_PAGE_SOUP = 'Loaded page soup was updated'
TAGS_LINK_ATTRS = {
    IMG: SRC,
    LINK: HREF,
    SCRIPT: SRC
}


logger = get_logger(__name__)


def download(url, output_path=os.getcwd()):
    loaded_page_full_path = get_loaded_main_page_file_full_path(
        url,
        output_path
    )
    logger.info(RECEIVED_LOADED_PAGE_FULL_PATH)

    response = get_response_for_request(url)
    original_html = response.text
    logger.info(RECEIVED_ORIGINAL_HTML)

    loaded_resources_dir_name = get_loaded_local_resources_dir_name(url)
    create_loaded_local_resources_dir(output_path, loaded_resources_dir_name)

    loaded_page_soup = BeautifulSoup(original_html, 'html.parser')
    logger.info(CREATED_LOADED_PAGE_SOUP)

    local_resources_count = len(
        [
            tag
            for tag, link_attr in TAGS_LINK_ATTRS.items()
            for tag in loaded_page_soup.find_all(tag)
            if is_local_resource(tag.get(link_attr), url)
        ]
    )
    bar = Bar(max=local_resources_count)

    for tag_name, link_attr in TAGS_LINK_ATTRS.items():
        for tag in loaded_page_soup.find_all(tag_name):
            tag_attr_link = tag.get(link_attr)

            if not is_local_resource(tag_attr_link, url):
                continue
            local_resource_relative_link = (
                get_local_resource_relative_link(tag_attr_link, url)
            )
            local_resource_abs_link = (
                get_local_resource_abs_link(tag_attr_link, url)
            )
            logger.info(
                RECEIVED_LOCAL_RESOURCE_LINK.format(local_resource_abs_link)
            )

            bar.message = local_resource_abs_link

            loaded_local_resource_path = (
                get_loaded_local_resource_file_path(
                    local_resource_relative_link, url
                )
            )
            logger.info(
                RECEIVED_LOADED_RESOURCE_PATH.format(local_resource_abs_link)
            )

            try:
                local_resource_link_request_response = (
                    get_response_for_request(local_resource_abs_link)
                )
            except Exception as exc:
                logger.warning(exc)
            else:
                write_loaded_local_resource(
                    local_resource_link_request_response,
                    os.path.join(output_path, loaded_local_resource_path)
                )
                logger.info(
                    LOADED_RESOURCE.format(local_resource_abs_link, output_path)
                )
                tag[link_attr] = loaded_local_resource_path
                logger.info(
                    CHANGED_RESOURCE_LINK.format(
                        local_resource_relative_link,
                        loaded_local_resource_path
                    )
                )

                bar.next()
            bar.finish()
    logger.info(UPDATED_LOADED_PAGE_SOUP)
    logger.info(LOADED_ALL_RESOURCES)

    prettified_loaded_page_soup = loaded_page_soup.prettify()
    write_loaded_main_page(loaded_page_full_path, prettified_loaded_page_soup)

    return loaded_page_full_path
