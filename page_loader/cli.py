import argparse
import os


DESCRIPTION = 'Load specified page'
OUTPUT_FLAG_HELP = 'output dir (default: working dir)'
OUTPUT_PATH = 'output_path'
PAGE_LOADER = 'page-loader'
URL = 'url'
URL_ARG_HELP = 'page url to load'
USAGE = '%(prog)s [options] <url>'


def parse_command_line_args():
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
    return page_loader_args_parser.parse_args()
