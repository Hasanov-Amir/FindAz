from sqlalchemy import String, Integer, SmallInteger
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import JSON, UUID, ARRAY

from database.base import Model, Column
from app.utils.helpers import create_hash
from app.exceptions.auth import InvalidPassword


class Product(Model):
    __tablename__ = "product"

    product_title = Column("product_title", String(30))
    product_owner_shop = Column("product_owner_shop", UUID(as_uuid=True))
    product_owner_shop_title = Column("product_owner_shop_title", String(50))
    product_count = Column("product_count", Integer())
    product_properties = Column("product_properties", JSON)
    product_images = Column("product_images", JSON)

    def __str__(self):
        return f"{self.id} : {self.product_title}"
    
    def __repr__(self):
        return f"{self.id} : {self.product_title}"


class User(Model):
    __tablename__ = "user"

    username = Column("username", String(20))
    first_name = Column("first_name", String(50))
    last_name = Column("last_name", String(50))
    password = Column("password", String(100))
    email = Column("email", String(320), unique=True, index=True)
    age = Column("age", SmallInteger())
    gender = Column("gender", String(20))
    profile_photo = Column("profile_photo", String(50))

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.password = create_hash(instance.password)
        return instance.save()

    def check_password(self, raw_password):
        hash_password = create_hash(raw_password)
        if self.password != hash_password:
            raise InvalidPassword("Invalid password")
        return True

    def __str__(self):
        return f"{self.id} : {self.email}"
    
    def __repr__(self):
        return f"{self.id} : {self.email}"


class TokenBlackList(Model):
    __tablename__ = "token_black_list"


class Shop(Model):
    __tablename__ = "shop"

    shop_title = Column("shop_title", String(50))
    shop_owner_id = Column("shop_owner_id", UUID(as_uuid=True), unique=True, index=True)
    shop_photo = Column("shop_photo", String(50))
    shop_tags = Column("shop_tags", MutableList.as_mutable(ARRAY(String)))
    shop_product_count = Column("shop_product_count", SmallInteger())

    def __str__(self):
        return f"id = {self.id}"
    
    def __repr__(self):
        return f"id = {self.id}"
