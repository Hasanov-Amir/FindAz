from werkzeug.serving import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

from app import create_app

flask_app = create_app()
app = DispatcherMiddleware(flask_app, {"/metrics": make_wsgi_app()})

if __name__ == "__main__":
    run_simple(
        "0.0.0.0", 8080, app, use_reloader=False, use_debugger=flask_app.config.get("DEBUG")
    )

