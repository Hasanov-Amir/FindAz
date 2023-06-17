from app.exceptions.base import JSONHTTPException


class InvalidID(JSONHTTPException):
    code = 400
    description = "Invalid ID"


class ProductNotFound(JSONHTTPException):
    code = 404
    description = "Product not found"
