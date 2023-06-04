from marshmallow import fields

from core.extensions import ma


class ProductSerializer(ma.Schema):
    id = fields.UUID(dump_only=True)
    create_date = fields.DateTime(dump_only=True)
    edit_date = fields.DateTime(dump_only=True)
    product_title = fields.Str(required=True)
    product_owner = fields.Str(required=True)
    product_count = fields.Int(required=True)
    product_properties = fields.Dict(required=True)


class ProductPutSerializer(ma.Schema):
    product_title = fields.Str(required=False)
    product_owner = fields.Str(required=False)
    product_count = fields.Int(required=False)
    product_properties = fields.Dict(required=False)
