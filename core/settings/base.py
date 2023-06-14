import os
from pathlib import Path

from cryptography.hazmat.primitives import serialization


class Config:
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')

    PROJECT_NAME = 'FindAz'

    MAX_CONTENT_LENGTH = 1_048_600
    IMAGE_ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    BASE_DIR = Path(__file__).parent.parent.parent

    MEDIA_PATH = os.path.join(BASE_DIR, 'app', 'public', 'media')

    LOG_FILENAME = os.path.join(BASE_DIR, 'logs', 'server.log')

    public_key_path = os.path.join(BASE_DIR, "core", "settings", "keys", "public.pem")
    private_key_path = os.path.join(BASE_DIR, "core", "settings", "keys", "private.pem")

    with open(public_key_path, 'rb') as f:
        public_key = serialization.load_pem_public_key(
            f.read()
        )
    
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None
        )
    
    PUBLIC_KEY = public_key
    PRIVATE_KEY = private_key
