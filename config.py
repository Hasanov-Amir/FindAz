import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent

load_dotenv()

# name
PROJECT_NAME = "FindAz"

# path to media
MEDIA_PATH = os.path.join(os.getcwd(), 'app', 'media')

if not os.path.isdir(MEDIA_PATH):
    os.mkdir(MEDIA_PATH)

# flask run configs
DEBUG = False
HOST = "0.0.0.0"
PORT = 8080

# database settings
MONGO_URI = "mongodb+srv://{user}:{password}@findazdb.jf7zxaw.mongodb.net/?retryWrites=true&w=majority"
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URL = MONGO_URI.format(user=MONGO_USER, password=MONGO_PASSWORD)
