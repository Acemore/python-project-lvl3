import os
import pytest
import stat
from requests.exceptions import ConnectionError, HTTPError, RequestException

from page_loader import download
from page_loader.helpers.io import (
    CREATING_DIR_PERMISSION_ERROR, NO_SUCH_DIR_ERROR
)
from page_loader.helpers.requests import (
    CONNECTION_ERROR, NOT_STATUS_CODE_200, REQUEST_EXCEPTION
)


FAKE_PATH = '/fake_path'
SITE_MAIN_PAGE_URL = 'https://page-loader.hexlet.repl.co'
STATUS_CODE_404 = 404


@pytest.mark.parametrize(
    'exc_type, exc_text',
    [
        (ConnectionError, CONNECTION_ERROR),
        (RequestException, REQUEST_EXCEPTION)
    ]
)
def test_requests_exceptions(requests_mock, temp_dir, exc_type, exc_text):
    requests_mock.get(SITE_MAIN_PAGE_URL, exc=exc_type)

    with pytest.raises(exc_type) as exc:
        download(SITE_MAIN_PAGE_URL, temp_dir.name)

        assert not os.listdir(temp_dir.name)

    assert str(exc.value) == exc_text.format(SITE_MAIN_PAGE_URL)


def test_not_status_code_200(requests_mock, temp_dir):
    requests_mock.get(SITE_MAIN_PAGE_URL, status_code=STATUS_CODE_404)

    with pytest.raises(HTTPError) as http_err:
        download(SITE_MAIN_PAGE_URL, temp_dir.name)

        assert not os.listdir(temp_dir.name)

    assert str(http_err.value) == (
        NOT_STATUS_CODE_200.format(SITE_MAIN_PAGE_URL, STATUS_CODE_404)
    )


def test_creating_dir_permission_error(requests_mock, temp_dir):
    requests_mock.get(SITE_MAIN_PAGE_URL)

    os.chmod(temp_dir.name, stat.S_IRUSR)
    with pytest.raises(PermissionError) as permission_err:
        download(SITE_MAIN_PAGE_URL, temp_dir.name)

        assert not os.listdir(temp_dir.name)

    assert str(permission_err.value) == (
        CREATING_DIR_PERMISSION_ERROR.format(temp_dir.name)
    )


def test_creating_dir_path_not_found_error(requests_mock, temp_dir):
    requests_mock.get(SITE_MAIN_PAGE_URL)

    fake_path = os.path.join(temp_dir.name, FAKE_PATH)
    with pytest.raises(FileNotFoundError) as file_not_found_err:
        download(SITE_MAIN_PAGE_URL, fake_path)

        assert not os.listdir(temp_dir.name)

    assert str(file_not_found_err.value) == NO_SUCH_DIR_ERROR.format(fake_path)
