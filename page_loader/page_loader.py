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


DOT = '.'


def get_loaded_file_full_path(url, output_path):
    if output_path.startswith(DOT):
        output_path = re.sub(DOT, os.getcwd(), output_path, count=1)

    loaded_file_name = get_hyphenated_name(url, HTML_EXT)

    return os.path.join(output_path, loaded_file_name)


def write_loaded_page(loaded_page_full_path, soup):
    with open(loaded_page_full_path, 'w') as loaded_page:
        loaded_page.write(soup)


def download(url, output_path=os.getcwd()):
    loaded_page_full_path = get_loaded_file_full_path(url, output_path)
    original_html = requests.get(url).text

    local_resources_dir_name = get_hyphenated_name(url, FILES_POSTFIX)
    os.mkdir(
        os.path.join(
            output_path,
            local_resources_dir_name
        )
    )

    loaded_page_soup = BeautifulSoup(original_html, 'html.parser')
    updated_loaded_page_soup = get_updated_soup(
        loaded_page_soup,
        url,
        output_path
    )
    write_loaded_page(loaded_page_full_path, updated_loaded_page_soup)

    return loaded_page_full_path
