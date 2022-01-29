#!/usr/bin/env python3

import argparse
import os
from page_loader import download


DESCRIPTION = 'Load specified page'
OUTPUT_FLAG_HELP = 'output dir (default: working dir)'
OUTPUT_PATH = 'output_path'
PAGE_LOADER = 'page-loader'
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

    print(download(page_loader_args.url, page_loader_args.output_path))


if __name__ == '__main__':
    main()
