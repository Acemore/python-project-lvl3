import os
import pytest
import requests_mock
import tempfile

from page_loader import download
from page_loader.helpers.working_with_fs import (
    get_loaded_local_resources_dir_name, get_loaded_main_page_file_full_path
)
from tests import SITE_MAIN_PAGE_URL


EXPECTED_CSS_NAME = 'page-loader-hexlet-repl-co-assets-application.css'
EXPECTED_CSS_PATH = 'tests/fixtures/expected.css'
EXPECTED_IMAGE_NAME = 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'
EXPECTED_IMAGE_PATH = 'tests/fixtures/expected.png'
EXPECTED_LOADED_HTML_FILE_NAME = 'ru-hexlet-io-courses.html'
EXPECTED_LOADED_PHP_FILE_NAME = 'ru-hexlet-io-courses.php'
EXPECTED_MAIN_PAGE_PATH = 'tests/fixtures/expected_main_page.html'
EXPECTED_SCRIPT_NAME = 'page-loader-hexlet-repl-co-script.js'
EXPECTED_SCRIPT_PATH = 'tests/fixtures/expected.js'
EXPECTED_SUBPAGE_NAME ='page-loader-hexlet-repl-co-courses.html'
EXPECTED_SUBPAGE_PATH = 'tests/fixtures/expected_subpage.html'
LOCAL_RESOURCES_DIR_CONTENT_LEN = 4
ORIGINAL_MAIN_PAGE_PATH = 'tests/fixtures/original_main_page.html'
SITE_CSS_URL = 'https://page-loader.hexlet.repl.co/assets/application.css'
SITE_IMAGE_URL = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
SITE_SCRIPT_URL = 'https://page-loader.hexlet.repl.co/script.js'
SITE_SUBPAGE_URL = 'https://page-loader.hexlet.repl.co/courses'
TEMP_DIR_CONTENT_LEN = 2
URL_WITH_HTML = 'http://ru.hexlet.io/courses.html'
URL_WITH_HTTP = 'http://ru.hexlet.io/courses'
URL_WITH_HTTPS = 'https://ru.hexlet.io/courses/'
URL_WITH_PHP = 'http://ru.hexlet.io/courses.php'


@pytest.mark.parametrize(
    'url, expected_loaded_file_name',
    [
        (URL_WITH_HTML, EXPECTED_LOADED_HTML_FILE_NAME),
        (URL_WITH_HTTPS, EXPECTED_LOADED_HTML_FILE_NAME), 
        (URL_WITH_HTTP, EXPECTED_LOADED_HTML_FILE_NAME),
        (URL_WITH_PHP, EXPECTED_LOADED_PHP_FILE_NAME)
    ]
)
def test_loaded_file_full_path(url, expected_loaded_file_name):
    with tempfile.TemporaryDirectory() as temp_dir:
        assert get_loaded_main_page_file_full_path(url, temp_dir) == (
            os.path.join(temp_dir, expected_loaded_file_name)
        )


def test_loaded_files():
    with open(ORIGINAL_MAIN_PAGE_PATH) as original_main_page:
        original_main_page_text = original_main_page.read()
    with open(EXPECTED_MAIN_PAGE_PATH) as expected_main_page:
        expected_loaded_page_text = expected_main_page.read()

    with open(EXPECTED_CSS_PATH) as expected_css:
        expected_css_text = expected_css.read()
    with open(EXPECTED_SUBPAGE_PATH) as expected_subpage:
        expected_subpage_text = expected_subpage.read()
    with open(EXPECTED_IMAGE_PATH, 'rb') as expected_image:
        expected_image_content = expected_image.read()
    with open(EXPECTED_SCRIPT_PATH) as expected_script:
        expected_script_text = expected_script.read()

    with tempfile.TemporaryDirectory() as temp_dir:
        with requests_mock.Mocker() as mock:
            mock.get(SITE_MAIN_PAGE_URL, text=original_main_page_text)
            mock.get(SITE_CSS_URL, text=expected_css_text)
            mock.get(SITE_SUBPAGE_URL, text=expected_subpage_text)
            mock.get(SITE_IMAGE_URL, content=expected_image_content)
            mock.get(SITE_SCRIPT_URL, text=expected_script_text)

            loaded_page_path = download(SITE_MAIN_PAGE_URL, temp_dir)

        local_resources_dir_name = (
            get_loaded_local_resources_dir_name(SITE_MAIN_PAGE_URL)
        )
        local_resources_dir_path = os.path.join(
            temp_dir,
            local_resources_dir_name
        )

        with open(loaded_page_path) as loaded_page:
            assert loaded_page.read() == expected_loaded_page_text

        with open(
            os.path.join(
                local_resources_dir_path,
                EXPECTED_CSS_NAME
                )
            ) as result_css:
            assert result_css.read() == expected_css_text
        with open(
            os.path.join(
                local_resources_dir_path,
                EXPECTED_SUBPAGE_NAME
                )
            ) as result_subpage:
            assert result_subpage.read() == expected_subpage_text
        with open(
            os.path.join(
                local_resources_dir_path,
                EXPECTED_IMAGE_NAME
                ),
                'rb'
            ) as result_image:
            assert result_image.read() == expected_image_content
        with open(
            os.path.join(
                local_resources_dir_path,
                EXPECTED_SCRIPT_NAME
                )
            ) as result_script:
            assert result_script.read() == expected_script_text

        assert len(os.listdir(temp_dir)) == TEMP_DIR_CONTENT_LEN
        assert len(os.listdir(local_resources_dir_path)) == (
            LOCAL_RESOURCES_DIR_CONTENT_LEN
        )
