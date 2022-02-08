import logging
from page_loader.page_loader import download


LOG_FILE = 'page_loader.log'
LOG_RECORD_FORMAT = '%(asctime)s :: %(levelname)s :: %(message)s'


__all__ = (
    download
)


def set_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        format=LOG_RECORD_FORMAT,
        level=logging.DEBUG
    )


set_logger()
