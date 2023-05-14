from app.main import bp
from .views import Index, GetMedia

bp.add_url_rule("/", view_func=Index.as_view("index"))
bp.add_url_rule("/<string:file>", view_func=GetMedia.as_view("get_media"))
