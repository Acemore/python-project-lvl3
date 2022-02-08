#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from page_loader import download, LOG_FILE
from page_loader.page_loader import KnownError


DESCRIPTION = 'Load specified page'
KNOWN_OCCURED_ERROR = "Some error occured. For details see '{}'"
OUTPUT_FLAG_HELP = 'output dir (default: working dir)'
OUTPUT_PATH = 'output_path'
PAGE_LOADER = 'page-loader'
SUCCESSFUL_LOADING = "Page was successfully downloaded into '{}'"
UNKNOWN_OCCURED_ERROR = "UNKNOWN error occured. For details see '{}'"
URL = 'url'
URL_ARG_HELP = 'page url to load'
USAGE = '%(prog)s [options] <url>'


def main():
    page_loader_args_parser = argparse.ArgumentParser(
        prog=PAGE_LOADER,
        usage=USAGE,
        description=DESCRIPTION,
    )
    page_loader_args_parser.add_argument(
        '-o', '--output',
        dest=OUTPUT_PATH,
        default=os.getcwd(),
        help=OUTPUT_FLAG_HELP
    )
    page_loader_args_parser.add_argument(URL, help=URL_ARG_HELP)
    page_loader_args = page_loader_args_parser.parse_args()

    try:
        loaded_page_full_path = download(
            page_loader_args.url,
            page_loader_args.output_path
        )
    except KnownError as known_error:
        logging.error(known_error)
        print(KNOWN_OCCURED_ERROR.format(LOG_FILE))
        sys.exit(1)
    except Exception as unknown_error:
        logging.error(unknown_error)
        print(UNKNOWN_OCCURED_ERROR.format(LOG_FILE))
        sys.exit(1)
    else:
        final_message = SUCCESSFUL_LOADING.format(loaded_page_full_path)
        logging.info(final_message)
        print(final_message)
        sys.exit(0)


if __name__ == '__main__':
    main()
