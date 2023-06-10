from flask import request
from marshmallow import ValidationError

from .serializer import UserSerializer
from app.data.models import User


def get_me():
    return


def login_user():
    data = request.json
    

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
