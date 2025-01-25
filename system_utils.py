
import logging

__all__ = ('init_logging')

def init_logging(file_name: str):
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s - %(message)s")
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(file_name, mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger('')
    root_logger.handlers.clear()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(file_handler)

    httpx_logger = logging.getLogger('httpx')
    httpx_logger.setLevel(logging.WARN)
    
    gbox_logger = logging.getLogger('gbox')
    gbox_logger.setLevel(logging.DEBUG)

