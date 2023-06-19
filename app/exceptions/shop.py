from .base import JSONHTTPException


class ShopAlreadyExist(JSONHTTPException):
    code = 400
    description = "Shop already exists"


class ShopNotFound(JSONHTTPException):
    code = 400
    description = "Shop not found"
