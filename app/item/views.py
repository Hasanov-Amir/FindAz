import uuid
from datetime import datetime

from flask.views import MethodView
from flask import request
from werkzeug.utils import secure_filename
from bson import ObjectId

from app.extensions import findaz_db
from config import MEDIA_PATH


class Items(MethodView):
    init_every_request = False
    methods = ["GET", "POST"]
    model = findaz_db.items

    def get(self, item_id=None):
        if item_id:
            item = list(self.model.find({"_id": ObjectId(item_id)}))
            item = list(map(lambda x: dict(x, **{'_id': str(x['_id'])}), item))
            return {"item": item[0]}
        else:
            items = list(self.model.find())
            items = list(map(lambda x: dict(x, **{'_id': str(x['_id'])}), items))
            return {"items": items}

    def post(self):
        data = request.json
        data.update({"time_added": datetime.now()})
        item = str(self.model.insert_one(data).inserted_id)
        return {"item_id": item}


class UploadItemPhoto(MethodView):
    init_every_request = False
    methods = ['PATCH']
    model = findaz_db.items
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def patch(self, item_id):
        file = request.files['file']

        try:
            item = self.model.find_one({"_id": ObjectId(item_id)})
        except Exception as e:
            error = f"Invalid item id.\nDetailed: {e}"
            return {"error": error}, 401

        if not item:
            error = "No item with this id"
            return {"error": error}, 404

        if file.filename == '':
            error = 'No file selected for uploading'
            return {"error": error}, 404

        if file and self.allowed_file(file.filename):
            file.filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
            file.filename = secure_filename(file.filename)
            file.save(f"{MEDIA_PATH}\\{file.filename}")
            self.model.update_one({"_id": ObjectId(item_id)}, {"$set": {"image_url": file.filename}})
            return {"image_url": file.filename}
        else:
            error = f'Allowed file types are {self.ALLOWED_EXTENSIONS}'
            return {"error": error}
