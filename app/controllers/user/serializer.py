from marshmallow import fields

from core.extensions import ma
from app.utils.field_types import PasswordType


class UserSerializer(ma.Schema):
    id = fields.UUID(dump_only=True)
    create_date = fields.DateTime(dump_only=True)
    edit_date = fields.DateTime(dump_only=True)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = PasswordType(load_only=True)
    age = fields.Int(required=False)
    gender = fields.Str(required=False)
    profile_photo = fields.Str(dump_only=True)
