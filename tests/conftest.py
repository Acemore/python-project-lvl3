import pytest
import tempfile
from requests import ConnectionError, HTTPError, RequestException

from tests import (
    EXPECTED_CSS_PATH, EXPECTED_IMAGE_PATH, EXPECTED_SCRIPT_PATH,
    EXPECTED_SUBPAGE_PATH, get_file_content, SITE_MAIN_PAGE_URL
)


ORIGINAL_MAIN_PAGE_PATH = 'tests/fixtures/original_main_page.html'
SITE_CSS_URL = 'https://page-loader.hexlet.repl.co/assets/application.css'
SITE_IMAGE_URL = (
    'https://page-loader.hexlet.repl.co/assets/professions/nodejs.png'
)
SITE_SCRIPT_URL = 'https://page-loader.hexlet.repl.co/script.js'
SITE_SUBPAGE_URL = 'https://page-loader.hexlet.repl.co/courses'


@pytest.fixture
def mock_main_page_and_its_local_resources_requests(requests_mock):
    original_main_page_text = get_file_content(ORIGINAL_MAIN_PAGE_PATH).decode()

    expected_css_text = get_file_content(EXPECTED_CSS_PATH).decode()
    expected_subpage_text = get_file_content(EXPECTED_SUBPAGE_PATH).decode()
    expected_image_content = get_file_content(EXPECTED_IMAGE_PATH)
    expected_script_text = get_file_content(EXPECTED_SCRIPT_PATH).decode()

    requests_mock.get(SITE_MAIN_PAGE_URL, text=original_main_page_text)
    requests_mock.get(SITE_CSS_URL, text=expected_css_text)
    requests_mock.get(SITE_SUBPAGE_URL, text=expected_subpage_text)
    requests_mock.get(SITE_IMAGE_URL, content=expected_image_content)
    requests_mock.get(SITE_SCRIPT_URL, text=expected_script_text)


@pytest.fixture
def mock_resources_requests_with_exceptions(requests_mock):
    original_main_page_text = get_file_content(ORIGINAL_MAIN_PAGE_PATH).decode()
    expected_script_text = get_file_content(EXPECTED_SCRIPT_PATH).decode()

    requests_mock.get(SITE_MAIN_PAGE_URL, text=original_main_page_text)
    requests_mock.get(SITE_CSS_URL, exc=ConnectionError)
    requests_mock.get(SITE_SUBPAGE_URL, exc=HTTPError)
    requests_mock.get(SITE_IMAGE_URL, exc=RequestException)
    requests_mock.get(SITE_SCRIPT_URL, text=expected_script_text)


@pytest.fixture
def temp_dir():
    return tempfile.TemporaryDirectory()
