from sqlalchemy import event
from sqlalchemy.orm import Session

from .models import Shop, Product


@event.listens_for(Product, 'after_insert')
@event.listens_for(Product, 'after_delete')
def update_product_count(mapper, connection, target):
    shop_uuid = target.product_owner_shop
    product_count = len(Product.filter(product_owner_shop=shop_uuid))
    session = Session(bind=connection)
    session.execute(
        Shop.__table__.update().where(Shop.id == shop_uuid).values(shop_product_count=product_count)
    )
    session.close()
