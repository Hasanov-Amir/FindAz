import json

from werkzeug.wrappers import Request, Response

from app.data.models import User
from app.utils.jwtutil import token_is_valid, decode_token
from app.exceptions.auth import (
    InvalidToken,
    ExpiredToken,
    InvalidTokenType,
    AccessTokenNotFound,
    RefreshTokenNotFound,
    InvalidCredentials,
    InvalidPassword
)


class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        auth_header = request.headers.get('Authorization')

        if not (auth_header and auth_header.startswith('Bearer ')):
            return self.app(environ, start_response)

        token = auth_header.split(' ')[1]
        required_token_type = 'access'

        if environ.get('REQUEST_URI') == '/api/user/token/refresh':
            required_token_type = 'refresh'

        try:
            token_is_valid(token, token_type=required_token_type)
        except (
            InvalidToken,
            ExpiredToken,
            InvalidTokenType,
            AccessTokenNotFound,
            RefreshTokenNotFound,
            InvalidCredentials,
            InvalidPassword
        ) as error:
            res = Response(
                json.dumps({"error": error.description}),
                mimetype= 'application/json',
                status=400
            )
            return res(environ, start_response)

        payload = decode_token(token)
        environ['user'] = payload
        return self.app(environ, start_response)
