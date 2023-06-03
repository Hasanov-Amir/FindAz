import uuid

from main import db


class Product(db.Model):
    id = db.Column(UUID(as_uuid=True), )
