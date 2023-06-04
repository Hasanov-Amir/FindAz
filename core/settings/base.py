import os
from pathlib import Path

project_name = "FindAz"


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")

    BASE_DIR = Path(__file__).parent.parent.parent

    MEDIA_PATH = os.path.join(BASE_DIR, 'app', 'public', 'media')

    LOG_FILENAME = f"/logs/{project_name}.log"
