import os

from flask import send_file, current_app


def get_image(file):
    path = os.path.join(current_app.config["MEDIA_PATH"], file)

    try:
        return send_file(path), 200
    except FileNotFoundError:
        error = "No such file"
    
    return {"error": error}, 404
