import os

project_name = "FindAz"

class Config:
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")

    LOG_FILENAME = f"/logs/{project_name}.log"
