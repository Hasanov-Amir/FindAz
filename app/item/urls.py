from app.item import bp
from .views import Items, UploadItemPhoto

bp.add_url_rule("/", view_func=Items.as_view("items"))
bp.add_url_rule("/<string:item_id>", view_func=Items.as_view("exact_item"))
bp.add_url_rule("/add-photo/<string:item_id>", view_func=UploadItemPhoto.as_view("exact_item_photo_upload"))
