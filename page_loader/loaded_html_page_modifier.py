import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from page_loader.hyphenated_str_getter import (
    get_hyphenated_name,
    get_hyphenated_str
)


FILES_POSTFIX = '_files'
IMG = 'img'
SRC = 'src'


def get_all_images_links(soup):
    return [img[SRC] for img in soup.find_all(IMG)]


def get_loaded_image_name(url, local_resource_link):
    netloc = urlparse(url).netloc
    hyphenated_netloc = get_hyphenated_str(netloc)

    local_resource_link_without_ext, ext = os.path.splitext(local_resource_link)
    hyphenated_local_resource_link_without_ext = (
        get_hyphenated_str(local_resource_link_without_ext)
    )

    return '{}{}{}'.format(
        hyphenated_netloc,
        hyphenated_local_resource_link_without_ext,
        ext
    )


def get_loaded_images_paths(url, local_resources_links):
    return list(
        map(
            lambda local_resource_link: os.path.join(
                get_hyphenated_name(url, FILES_POSTFIX),
                get_loaded_image_name(url, local_resource_link)
            ),
            local_resources_links
        )
    )


def get_local_resources_links(links):
    return list(
        filter(
            lambda link: not urlparse(link).netloc,
            links
        )
    )


def get_soup_with_loaded_images_links(soup, loaded_imgs_links):
    for img, loaded_image_link in zip(soup.find_all(IMG), loaded_imgs_links):
        img[SRC] = loaded_image_link

    return soup.prettify()


def get_soup(html_file_path):
    with open(html_file_path) as html_file:
        return BeautifulSoup(html_file, 'html.parser')


def update_loaded_page(loaded_page_full_path, soup):
    with open(loaded_page_full_path, 'w') as loaded_page:
        loaded_page.write(soup)
