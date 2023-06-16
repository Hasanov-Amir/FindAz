from marshmallow import fields

from core.extensions import ma
from app.utils.field_types import PasswordType, FileType


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

    def __init__(self, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if method == "POST_LOGIN":
            self.fields['username'].required = False
        
        if method == "PUT":
            self.fields['email'].required = False
            self.fields['email'].dump_only = True


class UserProfilePhotoSerializer(ma.Schema):
    profile_photo = FileType(required=True)


class UserPasswordChangeSerializer(ma.Schema):
    old_password = fields.Str(required=True)
    new_password1 = PasswordType(required=True)
    new_password2 = PasswordType(required=True)
