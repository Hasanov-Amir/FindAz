import uuid

from flask import request, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError

from app.data.models import Product
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
    request_method = request.method
    product_schema = ProductSerializer()
    product_put_schema = ProductSerializer(method=request_method)

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


def change_product_images(id):
    images = {file: request.files[file] for file in request.files}
    images_schema = ProductImagesSerializer()

    try:
        images_schema.load(images)
    except ValidationError as error:
        return {"error": error.messages}, 400

    try:
        product_id = uuid.UUID(id)
    except ValueError:
        return {"error": "Invalid id"}, 400

    product = Product.get(product_id)

    if not product:
        error = f"Product not found."
        return {"error": error}, 404

    for key, image in images.items():
        filename = image.filename
        
        filename = f"{uuid.uuid4()}.{filename.rsplit('.', 1)[1].lower()}"
        filename = secure_filename(filename)
        image.save(f"{current_app.config['MEDIA_PATH']}\\{filename}")

        images[key] = filename

    product.update(product_images=images)

    return images, 200


def delete_product(id):
    try:
        product_id = uuid.UUID(id)
    except ValueError:
        return {"error": "Invalid id"}, 400
    
    product = Product.get(product_id)

    if not product:
        return {"error": "Product not found"}, 404
    
    product.delete()

    return {}, 204
