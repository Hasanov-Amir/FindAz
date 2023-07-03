from app.exceptions.base import JSONHTTPException


class InvalidID(JSONHTTPException):
    code = 400
    description = "Invalid ID"


class ProductNotFound(JSONHTTPException):
    code = 404
    description = "Product not found"


class ProductImageFieldNotFound(JSONHTTPException):
    code = 404
    description = "Product does not have product_images field"


class ProductImageKeyFieldNotFound(JSONHTTPException):
    code = 404
    description = "product_images field does not have this field"


class ProductIsNotYour(JSONHTTPException):
    code = 403
    description = "Product is not your"
