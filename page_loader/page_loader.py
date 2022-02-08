import logging
import os
import re
import requests
from bs4 import BeautifulSoup

from page_loader.hyphenated_str_getter import get_hyphenated_name
from page_loader.page_loader_helper import (
    FILES_POSTFIX,
    HTML_EXT,
    get_updated_soup
)


CREATED_LOADED_PAGE_SOUP = 'Loaded page soup was received'
CREATED_LOADED_RESOURCES_FOLDER = 'Loaded resources folder was created'
DOT = '.'
LOADED_ALL_RESOURCES = 'All local resources were downloaded'
RECEIVED_ORIGINAL_HTML = 'Original html was received'
RECEIVED_LOADED_PAGE_FULL_PATH = 'Loaded page full path was received'
UPDATED_LOADED_PAGE_SOUP = 'Loaded page soup was updated'
WRITTEN_LOADED_PAGE = "Loaded page soup was written to '{}'"


class KnownError(Exception):
    pass


def get_loaded_file_full_path(url, output_path):
    if output_path.startswith(DOT):
        output_path = re.sub(DOT, os.getcwd(), output_path, count=1)

    loaded_file_name = get_hyphenated_name(url, HTML_EXT)

    return os.path.join(output_path, loaded_file_name)


def write_loaded_page(loaded_page_full_path, soup):
    with open(loaded_page_full_path, 'w') as loaded_page:
        loaded_page.write(soup)

    logging.info(WRITTEN_LOADED_PAGE.format(loaded_page_full_path))


def download(url, output_path=os.getcwd()):
    loaded_page_full_path = get_loaded_file_full_path(url, output_path)
    logging.info(RECEIVED_LOADED_PAGE_FULL_PATH)

    original_html = requests.get(url).text
    logging.info(RECEIVED_ORIGINAL_HTML)

    local_resources_dir_name = get_hyphenated_name(url, FILES_POSTFIX)
    os.mkdir(
        os.path.join(
            output_path,
            local_resources_dir_name
        )
    )
    logging.info(CREATED_LOADED_RESOURCES_FOLDER)

    loaded_page_soup = BeautifulSoup(original_html, 'html.parser')
    logging.info(CREATED_LOADED_PAGE_SOUP)
    updated_loaded_page_soup = get_updated_soup(
        loaded_page_soup,
        url,
        output_path
    )
    logging.info(UPDATED_LOADED_PAGE_SOUP)
    logging.info(LOADED_ALL_RESOURCES)
    write_loaded_page(loaded_page_full_path, updated_loaded_page_soup)

    return loaded_page_full_path
