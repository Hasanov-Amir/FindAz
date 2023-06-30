import os
import uuid

from flask import request, current_app
from sqlalchemy.orm.attributes import flag_modified
from werkzeug.utils import secure_filename
from marshmallow import ValidationError

from app.data.models import Product
from app.utils.helpers import valid_uuid
from app.exceptions.product import (
    ProductImageKeyFieldNotFound,
    ProductImageFieldNotFound,
    ProductNotFound
)
from .serializer import ProductSerializer, ProductImagesSerializer


def add_product():
    data = request.json
    product_schema = ProductSerializer()

    try:
        validated_data = product_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    product = Product.create(**validated_data)
    response = product_schema.dump(product)
    return response, 201


def get_product(id):
    product_id = valid_uuid(id)
    product = Product.get(product_id)
    product_schema = ProductSerializer()

    if not product:
        raise ProductNotFound("Product not found")
    
    response = product_schema.dump(product)
    return response, 200


def get_products():
    products = Product.filter()
    product_schema = ProductSerializer()
    response = product_schema.dump(products, many=True)
    return response, 200


def change_product(id):
    data = request.json
    request_method = request.method
    product_schema = ProductSerializer(method=request_method)
    product_id = valid_uuid(id)
    
    try:
        validated_data = product_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    product = Product.get(product_id)

    if not product:
        raise ProductNotFound("Product not found")
    
    ready_product = product.update(**validated_data)
    response = product_schema.dump(ready_product)
    return response, 200


def change_product_images(id):
    images = {file: request.files[file] for file in request.files}
    images_schema = ProductImagesSerializer()
    product_id = valid_uuid(id)

    try:
        images_schema.load(images)
    except ValidationError as error:
        return {"error": error.messages}, 400

    product = Product.get(product_id)

    if not product:
        raise ProductNotFound("Product not found")

    for key, image in images.items():
        filename = image.filename
        filename = f"{uuid.uuid4()}.{filename.rsplit('.', 1)[1].lower()}"
        filename = secure_filename(filename)
        image.save(f"{current_app.config['MEDIA_PATH']}\\{filename}")
        images[key] = filename

    p_images = product.product_images or {}
    p_images.update(images)
    flag_modified(product, "product_images") # никто не знает почему но это работает
    product.update(product_images=p_images)
    return images, 200


def delete_product_images(id, field):
    product_id = valid_uuid(id)
    product = Product.get(product_id)

    if not product:
        raise ProductNotFound("Product not found")
    
    product_images = product.product_images
    
    if not product_images:
        raise ProductImageFieldNotFound("Product does not have product_images field")
    
    image_filename = product_images.get(field, False)

    if not image_filename:
        raise ProductImageKeyFieldNotFound(f"product_images field does not have {field} field")

    product_images.pop(field)
    flag_modified(product, "product_images")
    product.save()
    
    os.remove(f"{current_app.config['MEDIA_PATH']}\\{image_filename}")
    return {}, 204


def delete_product(id):
    product_id = valid_uuid(id)
    product = Product.get(product_id)

    if not product:
        raise ProductNotFound("Product not found")

    product.delete()
    return {}, 204
