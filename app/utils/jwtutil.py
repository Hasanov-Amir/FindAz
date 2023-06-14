import uuid
import base64
from datetime import datetime, timedelta

import jwt
from flask import current_app
from jwt.exceptions import ExpiredSignatureError, DecodeError

from app.data.models import TokenBlackList, User


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


def token_is_valid(token, token_type='access'):
    current_time = datetime.now().timestamp()

    try:
        payload = decode_token(token)        
    except (ExpiredSignatureError, DecodeError):
        return False
    
    if not payload.get('type') == token_type:
        return False
    
    user = User.get(payload.get('id'))
    
    if not user:
        return False
    
    if 'exp' in payload and payload.get('exp') < current_time:
        return False
    
    if is_token_in_blacklist(token):
        return False 

    return True


def get_payload(token):
    payload = decode_token(token)

    return payload


def add_token_to_blacklist(refresh_token):
    if not token_is_valid(refresh_token, token_type='refresh'):
        return False
    
    payload = get_payload(refresh_token)
    TokenBlackList.create(id=payload.get('token_id'))

    return True


def is_token_in_blacklist(token):
    payload = get_payload(token)

    if not TokenBlackList.get(payload.get('token_id')):
        return False
    
    return True
