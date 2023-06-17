from flask import request
from marshmallow import ValidationError

from app.data.models import Shop
from app.controllers.shop.serializer import (
    ShopSerializer,
    ShopPhotoSerializer
)


def create_shop():
    user = request.environ.get('user')
    data = request.json()
    shop_schema = ShopSerializer()

    try:
        validated_data = shop_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    return


def get_shop(id):
    return


def change_shop(id):
    return


def delete_shop(id):
    return
