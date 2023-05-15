import os

from flask.views import View, MethodView
from flask import render_template, send_file

from config import MEDIA_PATH


class Index(View):
    init_every_request = False

    def dispatch_request(self):
        return render_template("index.html")


class GetMedia(MethodView):
    init_every_request = False
    methods = ["GET"]

    def get(self, file):
        path = os.path.join(MEDIA_PATH, file)
        try:
            return send_file(path), 200
        except FileNotFoundError:
            error = "No such file"
            return {"error": error}, 404
