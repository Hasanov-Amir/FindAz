import hmac
import base64
import hashlib

from flask import current_app


def valid_uuid(id):
    return True


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["IMAGE_ALLOWED_EXTENSIONS"]


def create_hash(raw_string):
    hash_string = hmac.new(
        bytes(current_app.config['SECRET_KEY'], 'utf-8'),
        msg=raw_string.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    hash_string = base64.b64encode(hash_string).decode()
    return hash_string

