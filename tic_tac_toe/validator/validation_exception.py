from flask import jsonify


class ValidationException(Exception):
    def __init__(self, message: str):
        self.message = message
        self.status_code = 400





