import os
import re
from urllib.parse import urlparse

from page_loader.helpers import EMPTY_STR, SLASH
from page_loader.logger import get_logger


CREATED_LOADED_RESOURCES_FOLDER = 'Loaded resources folder was created'
CREATING_DIR_PERMISSION_ERROR = (
    "You don't have permission to create dir here: '{}'"
)
DOT = '.'
EXT_REGEXP = r'\.[^.\/]+$'
FILES_POSTFIX = '_files'
HTML_EXT = '.html'
HYPHEN = '-'
NO_SUCH_DIR_ERROR = "No such directory: '{}'"
NOT_LETTER_AND_NOT_DIGIT_REGEXP = r'[^a-zA-Z0-9]'
OS_ERROR = "Some system error occured, path '{}'"
QUERY_STRING = r'\?[^?]+$'
SCHEME_END = '://'
WRITING_PERMISSION_ERROR = "You don't have permission to write file here: '{}'"
WRITTEN_LOADED_PAGE = "Loaded page soup was written to '{}'"


logger = get_logger(__name__)


def create_loaded_local_resources_dir(
    output_path, loaded_local_resources_dir_name
):
    loaded_resources_dir_full_path = os.path.join(
        output_path,
        loaded_local_resources_dir_name
    )

    if not os.path.exists(loaded_resources_dir_full_path):
        try:
            os.mkdir(loaded_resources_dir_full_path)
        except PermissionError:
            raise PermissionError(
                CREATING_DIR_PERMISSION_ERROR.format(output_path)
            )
        except FileNotFoundError:
            raise FileNotFoundError(NO_SUCH_DIR_ERROR.format(output_path))
        except OSError:
            raise OS_ERROR(OS_ERROR.format(output_path))

    logger.info(CREATED_LOADED_RESOURCES_FOLDER)


def download_local_resource(response, output_path):
    response_chunks = response.iter_content()

    try:
        with open(output_path, 'wb') as loaded_file:
            for response_chunk in response_chunks:
                loaded_file.write(response_chunk)
    except PermissionError:
        raise PermissionError(WRITING_PERMISSION_ERROR.format(output_path))
    except OSError:
        raise OSError(OS_ERROR.format(output_path))


def get_hyphenated_str(str):
    return re.sub(
        NOT_LETTER_AND_NOT_DIGIT_REGEXP,
        HYPHEN,
        str
    )


def get_loaded_local_resource_file_name(local_resource_link, url):
    netloc = urlparse(url).netloc
    hyphenated_netloc = get_hyphenated_str(netloc)

    local_resource_link = re.sub(
        QUERY_STRING,
        EMPTY_STR,
        local_resource_link,
        count=1
    )
    local_resource_link_without_ext, ext = os.path.splitext(local_resource_link)
    if not ext:
        ext = HTML_EXT

    hyphenated_local_resource_link_without_ext = (
        get_hyphenated_str(local_resource_link_without_ext)
    )

    return '{}{}{}'.format(
        hyphenated_netloc,
        hyphenated_local_resource_link_without_ext,
        ext
    )


def get_loaded_local_resource_file_path(local_resource_link, url):
    return os.path.join(
        get_loaded_local_resources_dir_name(url),
        get_loaded_local_resource_file_name(local_resource_link, url)
    )


def get_loaded_local_resources_dir_name(url):
    loaded_main_page_name = get_loaded_main_page_file_name(url)

    return re.sub(EXT_REGEXP, EMPTY_STR, loaded_main_page_name) + FILES_POSTFIX


def get_loaded_main_page_file_full_path(url, output_path):
    if output_path.startswith(DOT):
        output_path = re.sub(DOT, os.getcwd(), output_path, count=1)

    loaded_main_page_name = get_loaded_main_page_file_name(url)

    return os.path.join(output_path, loaded_main_page_name)


def get_loaded_main_page_file_name(url):
    scheme = urlparse(url).scheme + SCHEME_END
    url_without_scheme = re.sub(scheme, EMPTY_STR, url, count=1)

    if url_without_scheme.endswith(SLASH):
        url_without_scheme = url_without_scheme.rstrip(SLASH)

    url_path_ext = HTML_EXT
    if url_path := urlparse(url).path:
        _, ext = os.path.splitext(url_path)
        if ext:
            url_path_ext = ext

    url_without_scheme_and_ext = (
        re.sub(EXT_REGEXP, EMPTY_STR, url_without_scheme)
    )
    hyphenated_url_without_scheme = (
        get_hyphenated_str(url_without_scheme_and_ext)
    )
    return hyphenated_url_without_scheme + url_path_ext


def write_loaded_main_page(loaded_page_full_path, soup):
    try:
        with open(loaded_page_full_path, 'w') as loaded_page:
            loaded_page.write(soup)
    except PermissionError:
        raise PermissionError(
            WRITING_PERMISSION_ERROR.format(loaded_page_full_path)
        )
    except OSError:
        raise OSError(OS_ERROR.format(loaded_page_full_path))
    else:
        logger.info(WRITTEN_LOADED_PAGE.format(loaded_page_full_path))
