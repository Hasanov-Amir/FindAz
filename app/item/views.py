import uuid
from datetime import datetime

from flask.views import MethodView
from flask import request
from werkzeug.utils import secure_filename
from bson import ObjectId

from app.extensions import findaz_db
from .utils import check_file_size
from config import MEDIA_PATH, MEDIA_FILE_SIZE


class Items(MethodView):
    init_every_request = False
    methods = ["GET", "POST"]
    model = findaz_db.items

    def get(self, item_id=None):
        if item_id:
            item = list(self.model.find({"_id": ObjectId(item_id)}))
            item = list(map(lambda x: dict(x, **{'_id': str(x['_id'])}), item))
            return {"item": item[0]}, 200
        else:
            items = list(self.model.find())
            items = list(map(lambda x: dict(x, **{'_id': str(x['_id'])}), items))
            return {"items": items}, 200

    def post(self):
        data = request.json
        data.update({"time_added": datetime.now()})
        item = str(self.model.insert_one(data).inserted_id)
        return {"item_id": item}, 201


class UploadItemPhoto(MethodView):
    init_every_request = False
    methods = ['PATCH']
    model = findaz_db.items
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def patch(self, item_id):
        files = [[request.files[file], file] for file in request.files]
        names_ls = list(map(lambda x: x[1], files))
        added_files = {}

        try:
            item = self.model.find_one({"_id": ObjectId(item_id)})
        except Exception as e:
            error = f"Invalid item id.\nDetailed: {e}"
            return {"error": error}, 400

        if not item:
            error = "No item with this id"
            return {"error": error}, 404

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

            if file[0] and self.allowed_file(file[0].filename):
                file[0].filename = f"{uuid.uuid4()}.{file[0].filename.rsplit('.', 1)[1].lower()}"
                file[0].filename = secure_filename(file[0].filename)
                file[0].save(f"{MEDIA_PATH}\\{file[0].filename}")
                if file[1] == "main_file":
                    self.model.update_one({"_id": ObjectId(item_id)}, {"$set": {"main_file_url": file[0].filename}})
                    added_files.update({"main_file_url": file[0].filename})
                    continue
                self.model.update_one({"_id": ObjectId(item_id)}, {"$set": {f"image{index}_url": file[0].filename}})
                added_files.update({f"image{index}_url": file[0].filename})
            else:
                error = f'Allowed file types are {self.ALLOWED_EXTENSIONS}'
                return {"error": error}, 400

        return added_files, 200
