import re
from marshmallow import ValidationError, fields
from flask import current_app

from app.utils.helpers import allowed_extension


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
    

class PasswordType(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        if len(value) < 8:
            raise ValidationError("Password must contain at least 8 symbols.")

        if not re.search(r'[a-z]', value) or not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain uppercase and lowercase characters.")

        if not re.search(r'\d', value):
            raise ValidationError("Password must contain at least one digit.")

        if not re.search(r'[!@#$%^&*(),_.\-?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special symbol (@, #, $...).")

        if ' ' in value:
            raise ValidationError("Password can't contain whitespace symbol.")

        return value
    

class PriceType(fields.Decimal):
    def _deserialize(self, value, attr, data, **kwargs):
        value = super()._deserialize(value, attr, data, **kwargs)
        value = round(value, 2) # TODO: fix it later

        return value
