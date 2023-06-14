from flask import request
from marshmallow import ValidationError

from .serializer import UserSerializer
from app.data.models import User
from app.utils.jwtutil import (
    add_token_to_blacklist,
    create_tokens,
    token_is_valid,
    get_payload,
)
from app.data.models import User


def get_user():
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]

    if not token_is_valid(token):
        error = {
            'error': 'Invalid token.'
        }
        return error, 400
    
    payload = get_payload(token)
    return payload, 200


def create_user():
    data = request.json
    user_schema = UserSerializer()

    try:
        validated_data = user_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    user = User.create(**validated_data)
    response = user_schema.dump(user)
    return response, 201


def login_user():
    data = request.json
    user_schema = UserSerializer(method='POST_LOGIN')

    try:
        validated_data = user_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400

    try:
        user = User.filter(email=validated_data.get('email'))[0]
    except IndexError:
        error = {
            'error': 'Invalid login credentials.'
        }
        return error, 400
    
    user_data = user_schema.dump(user)

    if not user:
        error = {
            'error': 'Invalid login credentials.'
        }
        return error, 400
    
    if not user.check_password(validated_data.get('password')):
        error = {
            'error': 'Invalid password.'
        }
        return error, 400

    response = create_tokens(user_data)
    return response, 200


def logout_user():
    auth_header = request.headers.get('Authorization')

    if auth_header and auth_header.startswith('Bearer '):
        refresh_token = auth_header.split(' ')[1]

    if not add_token_to_blacklist(refresh_token):
        error = {
            'error': 'Invalid token'
        }
        return error, 400
    return {}, 204


def refresh_access_token():
    auth_header = request.headers.get('Authorization')
    user_schema = UserSerializer()

    if auth_header and auth_header.startswith('Bearer '):
        refresh_token = auth_header.split(' ')[1]

    if not token_is_valid(refresh_token, token_type='refresh'):
        error = {
            'error': 'Invalid token.'
        }
        return error, 400

    payload = get_payload(refresh_token)
    add_token_to_blacklist(refresh_token)
    
    user = User.get(payload.get('id'))
    user_data = user_schema.dump(user)
    response = create_tokens(user_data)
    return response, 200
