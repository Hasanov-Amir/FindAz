import os
from dotenv import load_dotenv

load_dotenv()

# name
PROJECT_NAME = "FindAz"

# path to media
MEDIA_PATH = os.path.join(os.getcwd(), 'media')
MEDIA_FILE_SIZE = 1_048_600  # in bytes 1048600 ≈ 1 megabyte
MAX_FILES_COUNT = 6  # including main file
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

if not os.path.isdir(MEDIA_PATH):
    os.mkdir(MEDIA_PATH)

# flask run configs
DEBUG = False
HOST = "0.0.0.0"
PORT = 8080

# old database settings
MONGO_URI = "mongodb+srv://{user}:{password}@findazdb.jf7zxaw.mongodb.net/?retryWrites=true&w=majority"
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_URL = MONGO_URI.format(user=MONGO_USER, password=MONGO_PASSWORD)


# database settings
POSTGRESQL_URI = "postgress://{username}:{password}@{host}:{port}/{database}?sslmode=prefer&connect_timeout=10".format(
    database="findaz",
    host="localhost",
    port="5432",
    username=os.getenv("POSTGRESQL_USERNAME"),
    password=os.getenv("POSTGRESQL_PASSWORD")
)
