import os
from pathlib import Path


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')

    PROJECT_NAME = 'FindAz'

    MAX_CONTENT_LENGTH = 1_048_600
    IMAGE_ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    BASE_DIR = Path(__file__).parent.parent.parent

    MEDIA_PATH = os.path.join(BASE_DIR, 'app', 'public', 'media')

    LOG_FILENAME = os.path.join(BASE_DIR, 'logs', 'server.log')
