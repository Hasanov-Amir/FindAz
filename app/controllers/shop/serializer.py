from marshmallow import fields

from core.extensions import ma
from app.utils.field_types import FileType


class ShopSerializer(ma.Schema):
    id = fields.UUID(dump_only=True)
    create_date = fields.DateTime(dump_only=True)
    edit_date = fields.DateTime(dump_only=True)
    shop_title = fields.Str(required=True)
    shop_owner_id = fields.Str(dump_only=True)
    shop_photo = fields.Str(dump_only=True)
    shop_tags = fields.List(fields.Str(), required=False)

    def __init__(self, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if method == "PUT":
            self.fields['shop_title'].required = False


class ShopPhotoSerializer(ma.Schema):
    shop_photo = FileType(required=True)
