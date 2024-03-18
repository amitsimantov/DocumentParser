import logging

BASE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class Logger:

    def __init__(self, name: str):
        self._name = name

    def get_logger(self):
        logger = logging.getLogger(self._name)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(BASE_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

