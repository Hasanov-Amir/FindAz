from werkzeug.exceptions import HTTPException


class ExpKeyWasNotFound(HTTPException):
    code = 400
    description = "Expiration key was not provided."


class ExpKeyError(HTTPException):
    code = 400
    description = "Token was expired."
