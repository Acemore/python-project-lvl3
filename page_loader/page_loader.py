import logging
import os
import sys
from bs4 import BeautifulSoup

from page_loader.helpers.working_with_fs import (
    create_loaded_local_resources_dir, get_loaded_local_resources_dir_name,
    get_loaded_main_page_file_full_path, write_loaded_main_page
)
from page_loader.helpers.working_with_requests import get_response_for_request
from page_loader.helpers.working_with_soup import get_updated_soup


CREATED_LOADED_PAGE_SOUP = 'Loaded page soup was received'
LOADED_ALL_RESOURCES = 'All local resources were downloaded'
LOG_RECORD_FORMAT = '%(asctime)s :: %(levelname)s :: %(message)s'
RECEIVED_ORIGINAL_HTML = 'Original html was received'
RECEIVED_LOADED_PAGE_FULL_PATH = 'Loaded page full path was received'
UPDATED_LOADED_PAGE_SOUP = 'Loaded page soup was updated'
WARNING = 'WARNING'


def download(url, output_path=os.getcwd(), log_level=WARNING):
    logging.basicConfig(format=LOG_RECORD_FORMAT, level=log_level.upper())
    logging.StreamHandler(sys.stderr)

    loaded_page_full_path = get_loaded_main_page_file_full_path(
        url,
        output_path
    )
    logging.info(RECEIVED_LOADED_PAGE_FULL_PATH)

    response = get_response_for_request(url)
    original_html = response.text
    logging.info(RECEIVED_ORIGINAL_HTML)

    loaded_resources_dir_name = get_loaded_local_resources_dir_name(url)
    create_loaded_local_resources_dir(output_path, loaded_resources_dir_name)

    loaded_page_soup = BeautifulSoup(original_html, 'html.parser')
    logging.info(CREATED_LOADED_PAGE_SOUP)
    updated_loaded_page_soup = get_updated_soup(
        loaded_page_soup,
        url,
        output_path
    )
    logging.info(UPDATED_LOADED_PAGE_SOUP)
    logging.info(LOADED_ALL_RESOURCES)
    write_loaded_main_page(loaded_page_full_path, updated_loaded_page_soup)

    return loaded_page_full_path
