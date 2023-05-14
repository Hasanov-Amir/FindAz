from flask import Blueprint

bp = Blueprint('item', __name__)

from app.item import urls
