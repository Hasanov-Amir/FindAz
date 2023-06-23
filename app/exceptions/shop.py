from .base import JSONHTTPException


class ShopAlreadyExist(JSONHTTPException):
    code = 400
    description = "Shop already exists"


class ShopNotFound(JSONHTTPException):
    code = 400
    description = "Shop not found"


class ShopForbidden(JSONHTTPException):
    code = 403
    description = "Forbidden shop"


class ShopPhotoNotFound(JSONHTTPException):
    code = 404
    description = "Shop photo not found"
