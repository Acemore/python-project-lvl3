import os
import re
import requests

from page_loader.hyphenated_str_getter import get_hyphenated_name
from page_loader.loaded_html_page_modifier import (
    FILES_POSTFIX,
    get_all_images_links,
    get_loaded_images_paths,
    get_local_resources_links,
    get_soup_with_loaded_images_links,
    get_soup,
    update_loaded_page
)


DOT = '.'
HTML_EXT = '.html'


def get_loaded_file_full_path(url, output_path):
    if output_path.startswith(DOT):
        output_path = re.sub(DOT, os.getcwd(), output_path, count=1)

    loaded_file_name = get_hyphenated_name(url, HTML_EXT)

    return os.path.join(output_path, loaded_file_name)


def download_image(url, output_path):
    response = requests.get(url)

    with open(output_path, 'wb') as loaded_image:
        loaded_image.write(response.content)


def download(url, output_path=os.getcwd()):
    loaded_page_full_path = get_loaded_file_full_path(url, output_path)
    response = requests.get(url)
    with open(loaded_page_full_path, 'w') as loaded_page:
        loaded_page.write(response.text)

    local_resources_dir_name = get_hyphenated_name(url, FILES_POSTFIX)
    os.mkdir(
        os.path.join(
            output_path,
            local_resources_dir_name
        )
    )

    loaded_page_soup = get_soup(loaded_page_full_path)
    images_links = get_all_images_links(loaded_page_soup)
    local_resources_links = get_local_resources_links(images_links)
    loaded_images_paths = get_loaded_images_paths(url, local_resources_links)
    updated_loaded_page_soup = get_soup_with_loaded_images_links(
        loaded_page_soup,
        loaded_images_paths
    )
    update_loaded_page(loaded_page_full_path, updated_loaded_page_soup)

    for local_resource_link, loaded_image_path in zip(
        local_resources_links,
        loaded_images_paths
    ):
        download_image(
            url + local_resource_link,
            os.path.join(
                output_path,
                loaded_image_path
            )
        )

    return loaded_page_full_path
