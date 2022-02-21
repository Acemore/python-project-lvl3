import logging
import sys


LOG_RECORD_FORMAT = '%(asctime)s :: %(levelname)s :: %(message)s'


def get_stream_handler():
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(logging.Formatter(LOG_RECORD_FORMAT))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)

    stream_handler = get_stream_handler()
    logger.addHandler(stream_handler)

    return logger
