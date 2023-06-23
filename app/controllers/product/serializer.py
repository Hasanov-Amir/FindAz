from marshmallow import fields
from app.utils.field_types import FileType

from core.extensions import ma


class ProductSerializer(ma.Schema):
    id = fields.UUID(dump_only=True)
    create_date = fields.DateTime(dump_only=True)
    edit_date = fields.DateTime(dump_only=True)
    product_title = fields.Str(required=True)
    product_owner = fields.Str(dump_only=True)
    product_count = fields.Int(required=True)
    product_properties = fields.Dict(required=True)
    product_images = fields.Dict(dump_only=True)

    def __init__(self, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if method == "PUT":
            self.fields['product_title'].required = False
            self.fields['product_count'].required = False
            self.fields['product_properties'].required = False


class ProductImagesSerializer(ma.Schema):
    main_image = FileType(required=False)
    image_1 = FileType(required=False)
    image_2 = FileType(required=False)
    image_3 = FileType(required=False)
    image_4 = FileType(required=False)
    image_5 = FileType(required=False)
    image_6 = FileType(required=False)
    image_7 = FileType(required=False)
    image_8 = FileType(required=False)
    image_9 = FileType(required=False)
    image_10 = FileType(required=False)
