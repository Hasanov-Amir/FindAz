import json

from werkzeug.wrappers import Response
from werkzeug.exceptions import HTTPException


class JSONHTTPException(HTTPException):
    def __init__(self, description=None, response=None, *args, **kwargs):
        if response is None:
            response = self.get_default_response()
        self.response = response
        super().__init__(*args, **kwargs)
        self.description = description

    def get_default_response(self):
        return Response(
            response=self.get_body(),
            status=self.code,
            headers=self.get_headers()
        )

    def get_body(self, *args):
        return json.dumps({"error": self.description})

    def get_headers(self, *args):
        return [("Content-Type", "application/json")]
