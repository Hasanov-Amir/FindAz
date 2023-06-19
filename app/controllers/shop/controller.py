from flask import request
from marshmallow import ValidationError

from app.data.models import Shop
from app.controllers.shop.serializer import (
    ShopSerializer,
    ShopPhotoSerializer
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
    print(data)
    print(validated_data)
    # shop = Shop.create(**validated_data)
    # response = shop_schema.dump(shop)
    return {}, 204


def get_shop(id):
    return


def change_shop(id):
    return


def delete_shop(id):
    return
