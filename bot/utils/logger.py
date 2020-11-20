import logging


def init_logger(logging_level):
    root = logging.getLogger(__name__)
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    format_str = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
    logging.basicConfig(format=format_str, level=logging_level)
