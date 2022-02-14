import os
import pytest
import requests
import stat
import tempfile

from page_loader import download
from page_loader.helpers import KnownError
from page_loader.helpers.working_with_fs import (
    CREATING_DIR_PERMISSION_ERROR, NO_SUCH_DIR_ERROR
)
from page_loader.helpers.working_with_requests import (
    CONNECTION_ERROR, IO_ERROR, NOT_STATUS_CODE_200, REQUEST_EXCEPTION
)
from tests import SITE_MAIN_PAGE_URL


FAKE_PATH = '/fake_path'
STATUS_CODE_404 = 404


@pytest.mark.parametrize(
    'exc_type, exc_text',
    [
        (requests.exceptions.ConnectionError, CONNECTION_ERROR),
        (IOError, IO_ERROR),
        (requests.exceptions.RequestException, REQUEST_EXCEPTION),        
    ]
)
def test_requests_exceptions(requests_mock, exc_type, exc_text):
    requests_mock.get(SITE_MAIN_PAGE_URL, exc=exc_type)

    with pytest.raises(KnownError) as known_err:
        with tempfile.TemporaryDirectory() as temp_dir:
            download(SITE_MAIN_PAGE_URL, temp_dir)

            assert not os.listdir(temp_dir)

    assert str(known_err.value) == exc_text.format(SITE_MAIN_PAGE_URL)


def test_not_status_code_200(requests_mock):
    requests_mock.get(SITE_MAIN_PAGE_URL, status_code=STATUS_CODE_404)

    with pytest.raises(KnownError) as known_err:
        with tempfile.TemporaryDirectory() as temp_dir:
            download(SITE_MAIN_PAGE_URL, temp_dir)

            assert not os.listdir(temp_dir)

    assert str(known_err.value) == (
        NOT_STATUS_CODE_200.format(SITE_MAIN_PAGE_URL, STATUS_CODE_404)
    )


def test_creating_dir_permission_error(requests_mock):
    requests_mock.get(SITE_MAIN_PAGE_URL)

    with tempfile.TemporaryDirectory() as temp_dir:
        os.chmod(temp_dir, stat.S_IRUSR)
        with pytest.raises(KnownError) as known_err:
            download(SITE_MAIN_PAGE_URL, temp_dir)

            assert not os.listdir(temp_dir)

        assert str(known_err.value) == (
            CREATING_DIR_PERMISSION_ERROR.format(temp_dir)
        )


def test_creating_dir_path_not_found_error(requests_mock):
    requests_mock.get(SITE_MAIN_PAGE_URL)

    with tempfile.TemporaryDirectory() as temp_dir:
        fake_path = os.path.join(temp_dir, FAKE_PATH)
        with pytest.raises(KnownError) as known_err:
            download(SITE_MAIN_PAGE_URL, fake_path)

            assert not os.listdir(temp_dir)

        assert str(known_err.value) == (NO_SUCH_DIR_ERROR.format(fake_path))
