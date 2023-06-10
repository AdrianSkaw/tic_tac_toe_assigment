from http.client import HTTPException


class ValidationException(HTTPException):

    def __init__(self, message):
        super().__init__(message)
        self.message = message
        self.status_code = 400