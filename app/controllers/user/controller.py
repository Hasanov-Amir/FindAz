from flask import request
from marshmallow import ValidationError

from .serializer import (
    UserSerializer,
    UserPasswordChangeSerializer
)
from app.data.models import User
from app.utils.jwtutil import (
    add_token_to_blacklist,
    create_tokens,
)
from app.utils.helpers import create_hash
from app.exceptions.auth import (
    InvalidCredentials,
    InvalidPassword,
    PasswordsDismatch
)


def get_user():
    user = request.environ.get('user')
    return user, 200


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
        raise InvalidCredentials("Invalid credentials")
    
    user_data = user_schema.dump(user)
    
    if not user.check_password(validated_data.get('password')):
        raise InvalidPassword("Invalid password")

    response = create_tokens(user_data)
    return response, 200


def logout_user():
    user = request.environ.get('user')
    add_token_to_blacklist(user.get('token_id'))
    return {}, 204


def refresh_access_token():
    user = request.environ.get('user')
    user_schema = UserSerializer()

    add_token_to_blacklist(user.get('token_id'))
    user = User.get(user.get('id'))

    user_data = user_schema.dump(user)
    response = create_tokens(user_data)
    return response, 200


def change_password():
    data = request.json()
    user = request.environ.get('user')
    pass_schema = UserPasswordChangeSerializer()

    try:
        validated_data = pass_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400

    user_obj = User.get(user.get('id'))
    user_obj.check_password(validated_data.get('old_password'))

    if validated_data.get('new_password1') != \
       validated_data.get('new_password2'):
        raise PasswordsDismatch("Passwords dismatch")

    hashed_password = create_hash(validated_data.get('new_password1'))
    user_obj.update(password=hashed_password)
    return {}, 204


def change_user_info():
    data = request.json()
    user = request.environ.get('user')
    user_schema = UserSerializer(method="PUT")

    try:
        validated_data = user_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    user_obj = User.get(user.get('id'))
    updated_user = user_obj.update(**validated_data)
    updated_user_data = user_schema.dump(updated_user)

    return updated_user_data, 200
