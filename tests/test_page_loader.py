import os
import pytest
import requests_mock
import tempfile
from page_loader import download
from page_loader.page_loader import get_loaded_file_full_path


EXPECTED_LOADED_FILE_NAME = 'ru-hexlet-io-courses.html'
FIRST_URL_WITH_HTTP = 'http://ru.hexlet.io/courses'
FIRST_URL_WITH_HTTPS = 'https://ru.hexlet.io/courses/'
SECOND_URL = 'https://page-loader.hexlet.repl.co'


@pytest.mark.parametrize(
    'url',
    [
        FIRST_URL_WITH_HTTPS,
        FIRST_URL_WITH_HTTP
    ]
)
def test_loaded_file_full_path(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        assert get_loaded_file_full_path(url, temp_dir) == (
            os.path.join(temp_dir, EXPECTED_LOADED_FILE_NAME)
        )


def test_loaded_file_content():
    with open('tests/fixtures/expected.html') as expected_html:
        expected_loaded_file_content = expected_html.read()

    with requests_mock.Mocker() as m:
        m.get(SECOND_URL, text=expected_loaded_file_content)

        with tempfile.TemporaryDirectory() as temp_dir:
            loaded_file_path = download(SECOND_URL, temp_dir)

            with open(loaded_file_path) as loaded_file:
                assert loaded_file.read() == expected_loaded_file_content
