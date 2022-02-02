import os
import pytest
import requests_mock
import tempfile

from page_loader import download
from page_loader.page_loader import get_loaded_file_full_path
from page_loader.hyphenated_str_getter import get_hyphenated_name
from page_loader.loaded_html_page_modifier import FILES_POSTFIX


EXPECTED_HTML_PATH = 'tests/fixtures/expected.html'
EXPECTED_LOADED_FILE_NAME = 'ru-hexlet-io-courses.html'
EXPECTED_LOADED_IMAGE_NAME = 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'
ORIGINAL_HTML_PATH = 'tests/fixtures/original.html'
SITE_IMAGE_URL = 'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
SITE_MAIN_PAGE_URL = 'https://page-loader.hexlet.repl.co'
URL_WITH_HTTP = 'http://ru.hexlet.io/courses'
URL_WITH_HTTPS = 'https://ru.hexlet.io/courses/'


@pytest.mark.parametrize(
    'url',
    [
        URL_WITH_HTTPS,
        URL_WITH_HTTP
    ]
)
def test_loaded_file_full_path(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        assert get_loaded_file_full_path(url, temp_dir) == (
            os.path.join(temp_dir, EXPECTED_LOADED_FILE_NAME)
        )


def test_loaded_files():
    with open(ORIGINAL_HTML_PATH) as original_html:
        original_html_content = original_html.read()

    with open(EXPECTED_HTML_PATH) as expected_html:
        expected_loaded_page_content = expected_html.read()

    with requests_mock.Mocker() as m:
        m.get(SITE_MAIN_PAGE_URL, text=original_html_content)
        m.get(SITE_IMAGE_URL)

        with tempfile.TemporaryDirectory() as temp_dir:
            loaded_page_path = download(SITE_MAIN_PAGE_URL, temp_dir)

            local_resources_dir_name = (
                get_hyphenated_name(SITE_MAIN_PAGE_URL, FILES_POSTFIX)
            )
            local_resources_dir_path = os.path.join(
                temp_dir,
                local_resources_dir_name
            )
            assert EXPECTED_LOADED_IMAGE_NAME in (
                os.listdir(local_resources_dir_path)
            )

            with open(loaded_page_path) as loaded_page:
                assert loaded_page.read() == expected_loaded_page_content
