from marshmallow import ValidationError, fields
from flask import current_app

from app.utils.helpers import allowed_extension
from core.extensions import ma


class ProductSerializer(ma.Schema):
    id = fields.UUID(dump_only=True)
    create_date = fields.DateTime(dump_only=True)
    edit_date = fields.DateTime(dump_only=True)
    product_title = fields.Str(required=True)
    product_owner = fields.Str(required=True)
    product_count = fields.Int(required=True)
    product_properties = fields.Dict(required=True)
    product_images = fields.Dict(dump_only=True)

    def __init__(self, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if method == "PUT":
            self.fields['product_title'].required = False
            self.fields['product_owner'].required = False
            self.fields['product_count'].required = False
            self.fields['product_properties'].required = False


class FileType(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        filename = value.filename

        if not filename:
            error = 'No file selected for uploading.'
            raise ValidationError(error)

        if not allowed_extension(filename):
            error = f'Allowed file types are {current_app.config["IMAGE_ALLOWED_EXTENSIONS"]}.'
            raise ValidationError(error)

        return value


class ProductImagesSerializer(ma.Schema):
    main_image = FileType(required=True)
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
