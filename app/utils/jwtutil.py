import uuid
import base64
from datetime import datetime, timedelta

import jwt
from flask import current_app
from jwt.exceptions import ExpiredSignatureError, DecodeError

from app.data.models import TokenBlackList, User
from app.exceptions.auth import ExpiredToken, InvalidToken, InvalidTokenType


def create_token(payload):
    raw_token = jwt.encode(payload, current_app.config['PRIVATE_KEY'], algorithm='RS256')
    encrypted_token = base64.b64encode(bytes(raw_token, 'utf-8')).decode()
    return encrypted_token


def decode_token(encrypted_token):
    raw_token = base64.b64decode(encrypted_token).decode()
    payload = jwt.decode(raw_token, current_app.config['PUBLIC_KEY'], algorithms='RS256')
    return payload


def create_access_token(payload):
    exp = datetime.now() + timedelta(minutes=10)

    payload.update({
        "type": "access",
        "exp": int(exp.timestamp())
    })

    access_token = create_token(payload)
    return access_token


def create_refresh_token(payload):
    exp = datetime.now() + timedelta(days=7)

    payload.update({
        "type": "refresh",
        "exp": int(exp.timestamp())
    })

    refresh_token = create_token(payload)
    return refresh_token


def create_tokens(payload):
    token_id = str(uuid.uuid4())

    payload.update({
        "token_id": token_id
    })

    tokens = {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token({
            "token_id": token_id,
            "id": payload.get("id")
        })
    }
    return tokens


def is_token_type_access(payload, default_type="access"):
    token_type = payload.get('type')

    if token_type != default_type:
        raise InvalidTokenType(f"Invalid token type, {default_type} token is required.")
    return True


def token_is_valid(token, check_type=True, token_type='access'):
    current_time = datetime.now().timestamp()

    try:
        payload = decode_token(token)        
    except (ExpiredSignatureError, DecodeError):
        raise InvalidToken("Invalid token")

    if check_type:
        is_token_type_access(payload, default_type=token_type)

    user = User.get(payload.get('id'))

    if not user:
        raise InvalidToken("Invalid token")

    if 'exp' in payload and payload.get('exp') < current_time:
        raise ExpiredToken("Expired token")

    is_token_in_blacklist(payload.get('token_id'))
    return True


def add_token_to_blacklist(token_id):
    TokenBlackList.create(id=token_id)
    return True


def is_token_in_blacklist(token_id):
    if TokenBlackList.get(token_id):
        raise InvalidToken("Invalid token")
    return True
