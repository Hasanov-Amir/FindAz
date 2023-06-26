from sqlalchemy import event

from .models import Shop, Product


@event.listens_for(Product, 'after_insert')
@event.listens_for(Product, 'after_delete')
def update_product_count(mapper, connection, target):
    shop_uuid = target.product_owner_shop
    product_count = Product.filter(product_owner_shop=shop_uuid).count()
    Shop.get(shop_uuid).update(product_count=product_count)
