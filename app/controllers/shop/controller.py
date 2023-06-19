from flask import request
from marshmallow import ValidationError

from app.data.models import Shop
from app.controllers.shop.serializer import (
    ShopSerializer,
    ShopPhotoSerializer
)
from app.exceptions.shop import (
    ShopAlreadyExist,
    ShopNotFound
)


def create_shop():
    user = request.environ.get('user')
    data = request.json
    shop_schema = ShopSerializer()

    try:
        validated_data = shop_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    validated_data['shop_owner_id'] = user.get('id')

    if Shop.filter(shop_owner_id=user.get('id')):
        raise ShopAlreadyExist("Shop already exists")

    shop = Shop.create(**validated_data)
    response = shop_schema.dump(shop)
    return response, 200


def get_shop(id):
    shop_schema = ShopSerializer()
    shop = Shop.get(id)

    if not shop:
        raise ShopNotFound("Shop not found")
    
    response = shop_schema.dump(shop)
    return response, 200


def get_list_of_shops():
    return


def change_shop(id):
    return


def delete_shop(id):
    return
