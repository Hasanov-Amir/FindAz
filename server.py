import os

from werkzeug.serving import run_simple
from dotenv import load_dotenv

from core.factories import create_app, SettingsError

load_dotenv()

if setting := os.getenv("APP_SETTINGS"):
    settings_name = setting
else:
    raise SettingsError()
flask_app = create_app(settings_name)

if __name__ == '__main__':
    run_simple(
        "0.0.0.0",
        8080,
        flask_app,
        use_reloader=False,
        use_debugger=flask_app.config["DEBUG"]
    )
