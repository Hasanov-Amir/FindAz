from flask import Flask
from flask_cors import CORS

from app.extensions import findaz_db


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.item import bp as item_bp
    app.register_blueprint(item_bp, url_prefix='/api/items')

    return app
