#!/usr/bin/env python3

import sys
from requests.exceptions import ConnectionError, HTTPError, RequestException

from page_loader import download
from page_loader.cli import parse_command_line_args
from page_loader.logger import get_logger


EXCEPTION = "Unable to download resource '{}'. Unknown error occured: {}"
KNOWN_OCCURED_ERROR = "Some error occured. For details see '{}'"
SUCCESSFUL_LOADING = "Page was successfully downloaded into '{}'"
UNKNOWN_OCCURED_ERROR = "UNKNOWN error occured. For details see '{}'"


logger = get_logger(__name__)


def main():  # noqa C901
    page_loader_args = parse_command_line_args()

    try:
        loaded_page_full_path = download(
            page_loader_args.url,
            page_loader_args.output_path
        )
    except PermissionError as permission_err:
        logger.error(permission_err)
        print(permission_err)
        sys.exit(1)
    except FileNotFoundError as file_not_found_err:
        logger.error(file_not_found_err)
        print(file_not_found_err)
        sys.exit(1)
    except ConnectionError as connection_err:
        logger.error(connection_err)
        print(connection_err)
        sys.exit(1)
    except HTTPError as http_err:
        logger.error(http_err)
        print(http_err)
        sys.exit(1)
    except RequestException as request_exc:
        logger.error(request_exc)
        print(request_exc)
        sys.exit(1)
    except OSError as os_err:
        logger.error(os_err)
        print(os_err)
        sys.exit(1)
    except Exception as exception:
        logger.error(
            EXCEPTION.format(
                page_loader_args.url,
                exception
            )
        )
        sys.exit(1)
    else:
        final_message = SUCCESSFUL_LOADING.format(loaded_page_full_path)
        logger.info(final_message)
        print(final_message)
        sys.exit(0)


if __name__ == '__main__':
    main()
