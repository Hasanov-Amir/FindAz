import os
import uuid
from datetime import datetime

from bson import ObjectId
from bson.errors import InvalidId
from flask import request, send_file
from werkzeug.utils import secure_filename

from .model import findaz_db
from config import ALLOWED_EXTENSIONS, MAX_FILES_COUNT, MEDIA_FILE_SIZE, MEDIA_PATH
from .utils import check_file_size


def get_items():
    items = list(findaz_db.items.find())
    items = list(map(lambda x: dict(x, **{'_id': str(x['_id'])}), items))
    return {"items": items}, 200


def post_item():
    data = request.json
    data.update({"time_added": datetime.now()})
    item = str(findaz_db.items.insert_one(data).inserted_id)
    return {"item_id": item}, 201


def get_item(item_id):
    item = list(findaz_db.items.find({"_id": ObjectId(item_id)}))
    item = list(map(lambda x: dict(x, **{'_id': str(x['_id'])}), item))
    return {"item": item[0]}, 200


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def put_image_to_item(item_id):
    files = [[request.files[file], file] for file in request.files]
    names_ls = list(map(lambda x: x[1], files))
    added_files = {}

    try:
        item = findaz_db.items.find_one({"_id": ObjectId(item_id)})
    except InvalidId:
        error = f"Invalid item id."
        return {"error": error}, 400

    if not item:
        error = "No item with this id"
        return {"error": error}, 404

    if len(files) > MAX_FILES_COUNT:
        error = f"Too many files for item"
        return {"error": error}, 400

    if "main_file" not in names_ls:
        error = "main_file field is required"
        return {"error": error}, 400

    for index, file in enumerate(files):
        size = check_file_size(file[0])

        if size > MEDIA_FILE_SIZE:
            error = f'file size must be lower than {MEDIA_FILE_SIZE} bytes'
            return {"error": error}, 400

        if file[0].filename == "":
            error = 'no file selected for uploading'
            return {"error": error}, 404

        if file[0] and allowed_file(file[0].filename):
            file[0].filename = f"{uuid.uuid4()}.{file[0].filename.rsplit('.', 1)[1].lower()}"
            file[0].filename = secure_filename(file[0].filename)
            file[0].save(f"{MEDIA_PATH}\\{file[0].filename}")
            if file[1] == "main_file":
                findaz_db.items.update_one({"_id": ObjectId(item_id)}, {"$set": {"main_file_url": file[0].filename}})
                added_files.update({"main_file_url": file[0].filename})
                continue
            findaz_db.items.update_one({"_id": ObjectId(item_id)}, {"$set": {f"image{index}_url": file[0].filename}})
            added_files.update({f"image{index}_url": file[0].filename})
        else:
            error = f'Allowed file types are {ALLOWED_EXTENSIONS}'
            return {"error": error}, 400

    return added_files, 200


def get_image(file):
    path = os.path.join(MEDIA_PATH, file)
    try:
        return send_file(path), 200
    except FileNotFoundError:
        error = "No such file"
        return {"error": error}, 404
