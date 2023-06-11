from flask import jsonify


class ValidationException:

    def response(self, message):
        response = jsonify({'error': message})
        response.status_code = 400
        return response
