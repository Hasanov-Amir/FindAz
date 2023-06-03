from connexion import FlaskApp
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import argparse

from config import HOST, PORT, POSTGRESQL_URI

parser = argparse.ArgumentParser(description='Flask app',
                                 epilog='©Amir Hasanov all rights reserved')
parser.add_argument("--debug", action="store_true", help="Turns on debug mode")
parser.add_argument("--host", default=HOST, help="Define custom host")
parser.add_argument("--port", type=int, default=PORT, help="Define custom port")
args = parser.parse_args()

app = FlaskApp(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRESQL_URI
db.init_app(app)

app.add_api("api.yaml")

CORS(app.app, resources={r"/": {"origins": "*"}})

if __name__ == "__main__":
    app.run(host=args.host, port=args.port, debug=args.debug)
