import logging
from flask import request, session

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.clientip = request.remote_addr
        record.path = request.full_path
        record.method = request.method
        record.http_version = request.environ.get('SERVER_PROTOCOL')
        record.username = session.get('username', 'anonymous')
        return super().format(record)

def setup_logging(app):
    formatter = RequestFormatter(
        '%(clientip)s - - [%(asctime)s] "%(method)s %(path)s %(http_version)s" - User: %(username)s - %(message)s',
        datefmt='%d/%b/%Y %H:%M:%S'
    )
    handler = logging.FileHandler('logs/buyers.txt')
    handler.setFormatter(formatter)
    app_logger = logging.getLogger('app')
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(handler)

    @app.before_request
    def log_request_info():
        app.logger.info('Request')

    @app.after_request
    def log_response_info(response):
        app.logger.info('Response %d', response.status_code)
        return response

    return app_logger