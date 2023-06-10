from flask import current_app


def valid_uuid(id):
    return True


def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["IMAGE_ALLOWED_EXTENSIONS"]
