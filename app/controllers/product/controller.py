import uuid
from flask import make_response, request
from marshmallow import ValidationError

from app.data.models import Product
from .serializer import ProductSerializer, ProductPutSerializer


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
    try:
        product_id = uuid.UUID(id)
    except ValueError:
        return {"error": "Invalid id"}, 400
    
    product = Product.get(product_id)
    product_schema = ProductSerializer()

    if not product:
        return {"error": "Product not found"}, 404
    
    response = product_schema.dump(product)

    return response, 200


def get_products():
    products = Product.filter()
    product_schema = ProductSerializer()
    response = product_schema.dump(products, many=True)
    return response, 200


def change_product(id):
    data = request.json
    product_schema = ProductSerializer()
    product_put_schema = ProductPutSerializer()

    try:
        product_id = uuid.UUID(id)
    except ValueError:
        return {"error": "Invalid id"}, 400
    
    try:
        validated_data = product_put_schema.load(data)
    except ValidationError as error:
        return {"error": error.messages}, 400
    
    product = Product.get(product_id)

    if not product:
        return {"error": "Product not found"}, 404
    
    ready_product = product.update(**validated_data)
    response = product_schema.dump(ready_product)

    return response, 200


def delete_product(id):
    try:
        product_id = uuid.UUID(id)
    except ValueError:
        return {"error": "Invalid id"}, 400
    
    product = Product.get(product_id)

    if not product:
        return {"error": "Product not found"}, 404
    
    product.delete()
    response = make_response()
    response.status_code = 204
    return response
