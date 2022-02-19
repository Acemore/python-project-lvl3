import os
import pytest

from page_loader import download
from page_loader.helpers.working_with_fs import (
    get_loaded_local_resources_dir_name, get_loaded_main_page_file_full_path
)
from tests import (
    EXPECTED_CSS_PATH, EXPECTED_IMAGE_PATH, EXPECTED_SCRIPT_PATH,
    EXPECTED_SUBPAGE_PATH, get_file_content, R, RB, SITE_MAIN_PAGE_URL
)


EXPECTED_CSS_NAME = 'page-loader-hexlet-repl-co-assets-application.css'
EXPECTED_IMAGE_NAME = 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'
EXPECTED_LOADED_HTML_FILE_NAME = 'ru-hexlet-io-courses.html'
EXPECTED_LOADED_PHP_FILE_NAME = 'ru-hexlet-io-courses.php'
EXPECTED_MAIN_PAGE_PATH = 'tests/fixtures/expected_main_page.html'
EXPECTED_SCRIPT_NAME = 'page-loader-hexlet-repl-co-script.js'
EXPECTED_SUBPAGE_NAME = 'page-loader-hexlet-repl-co-courses.html'
LOCAL_RESOURCES_DIR_CONTENT_LEN = 4
ORIGINAL_MAIN_PAGE_PATH = 'tests/fixtures/original_main_page.html'
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
def test_loaded_file_full_path(temp_dir, url, expected_loaded_file_name):
    assert get_loaded_main_page_file_full_path(url, temp_dir.name) == (
        os.path.join(temp_dir.name, expected_loaded_file_name)
    )


def test_loaded_page(
    mock_main_page_and_its_local_resources_requests, temp_dir
):
    expected_loaded_page_text = get_file_content(EXPECTED_MAIN_PAGE_PATH)
    loaded_page_path = download(SITE_MAIN_PAGE_URL, temp_dir.name)

    assert get_file_content(loaded_page_path) == expected_loaded_page_text


@pytest.mark.parametrize(
    'expected_file_name, reading_mode, expected_file_content',
    [
        (EXPECTED_CSS_NAME, R, get_file_content(EXPECTED_CSS_PATH)),
        (EXPECTED_SUBPAGE_NAME, R, get_file_content(EXPECTED_SUBPAGE_PATH)),
        (EXPECTED_IMAGE_NAME, RB, get_file_content(EXPECTED_IMAGE_PATH, RB)),
        (EXPECTED_SCRIPT_NAME, R, get_file_content(EXPECTED_SCRIPT_PATH))
    ]
)
def test_loaded_local_resources(
    mock_main_page_and_its_local_resources_requests, temp_dir,
    expected_file_name, reading_mode, expected_file_content
):
    download(SITE_MAIN_PAGE_URL, temp_dir.name)

    local_resources_dir_name = (
        get_loaded_local_resources_dir_name(SITE_MAIN_PAGE_URL)
    )
    local_resources_dir_path = os.path.join(
        temp_dir.name,
        local_resources_dir_name
    )

    result_file_path = os.path.join(
        local_resources_dir_path,
        expected_file_name
    )
    assert get_file_content(result_file_path, reading_mode) == (
        expected_file_content
    )

    assert len(os.listdir(temp_dir.name)) == TEMP_DIR_CONTENT_LEN
    assert len(os.listdir(local_resources_dir_path)) == (
        LOCAL_RESOURCES_DIR_CONTENT_LEN
    )
