from app.exceptions.base import JSONHTTPException


class InvalidToken(JSONHTTPException):
    code = 400
    description = "Invalid token"


class ExpiredToken(JSONHTTPException):
    code = 400
    description = "Expired token"


class InvalidTokenType(JSONHTTPException):
    code = 400
    description = "Invalid token type"


class AccessTokenNotFound(JSONHTTPException):
    code = 400
    description = "This endpoint requires access token"


class RefreshTokenNotFound(JSONHTTPException):
    code = 400
    description = "This endpoint requires refresh token"


class InvalidCredentials(JSONHTTPException):
    code = 400
    description = "Invalid credentials"


class InvalidPassword(JSONHTTPException):
    code = 400
    description = "Invalid password"


class PasswordsDismatch(JSONHTTPException):
    code = 400
    description = "Passwords dismatch"
