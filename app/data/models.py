from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSON

from database.base import Model, Column


class Product(Model):
    __tablename__ = "product"

    product_title = Column("title", String(30))
    product_owner = Column("owner", String(50))
    product_count = Column("count", Integer())
    product_properties = Column("properties", JSON)

    def __str__(self):
        return f"{self.id} : {self.product_title}"
    
    def __repr__(self):
        return f"{self.id} : {self.product_title}"
