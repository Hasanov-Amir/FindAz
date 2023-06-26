import os
import uuid

from flask import request, current_app
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from app.data.models import Shop
from app.controllers.shop.serializer import (
    ShopSerializer,
    ShopPhotoSerializer
)
from app.exceptions.shop import (
    ShopAlreadyExist,
    ShopNotFound,
    ShopForbidden,
    ShopPhotoNotFound
)
from core.extensions import db
from app.utils.helpers import valid_uuid


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
    shop_id = valid_uuid(id)
    shop = Shop.get(shop_id)

    if not shop:
        raise ShopNotFound("Shop not found")
    
    response = shop_schema.dump(shop)
    return response, 200


def get_shops():
    shop_schema = ShopSerializer()
    shops = Shop.filter()
    response = shop_schema.dump(shops, many=True)
    return response, 200


def change_shop(id):
    user = request.environ.get('user')
    shop_id = valid_uuid(id)
    shop = Shop.get(shop_id)
    shop_schema = ShopSerializer(method="PUT")
    data = request.json

    if not shop:
        raise ShopNotFound("Shop not found")

    if shop.shop_owner_id != user.get('id'):
        raise ShopForbidden("Shop forbidden")
    
    try:
        validated_data = shop_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400

    updated_shop = shop.update(**validated_data)
    response = shop_schema.dump(updated_shop)
    return response, 200


def delete_shop(id):
    user = request.environ.get('user')
    shop_id = valid_uuid(id)
    shop = Shop.get(shop_id)

    if not shop:
        raise ShopNotFound("Shop not found")

    if shop.shop_owner_id != user.get('id'):
        raise ShopForbidden("Shop forbidden")
    
    shop.delete()
    return {}, 204


def set_shop_photo(id):
    user = request.environ.get('user')
    data = {'shop_photo': request.files['shop_photo']}
    shop_id = valid_uuid(id)
    shop = Shop.get(shop_id)
    shop_photo_schema = ShopPhotoSerializer()

    if not shop:
        raise ShopNotFound("Shop not found")
    
    if str(shop.shop_owner_id) != user.get('id'):
        raise ShopForbidden("Shop forbidden")

    try:
        validated_data = shop_photo_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    shop_photo = validated_data.get('shop_photo')
    filename = shop_photo.filename
    filename = f"{uuid.uuid4()}.{filename.rsplit('.', 1)[1].lower()}"
    filename = secure_filename(filename)
    shop_photo.save(f"{current_app.config['MEDIA_PATH']}\\{filename}")
    
    shop.update(shop_photo=filename)
    return {"shop_photo": filename}, 200


def delete_shop_photo(id, filename):
    user = request.environ.get('user')
    shop_id = valid_uuid(id)
    shop = Shop.get(shop_id)

    if not shop:
        raise ShopNotFound("Shop not found")
    
    if shop.shop_owner_id != user.get('id'):
        raise ShopForbidden("Shop forbidden")
    
    if shop.get('shop_photo') != filename:
        raise ShopPhotoNotFound("Shop photo not found")
    
    shop.update(shop_photo='')
    os.remove(f"{current_app.config['MEDIA_PATH']}\\{filename}")
    return {}, 204
