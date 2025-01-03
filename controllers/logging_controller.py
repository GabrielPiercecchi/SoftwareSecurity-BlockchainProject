import logging
from flask import request

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.clientip = request.remote_addr
        record.path = request.path
        return super().format(record)

def setup_logging():
    formatter = RequestFormatter('%(asctime)s - IP: %(clientip)s - Path: %(path)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler('logs/buyers.txt')
    handler.setFormatter(formatter)
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(handler)
    return app_logger