# import asyncio
# from typing import Optional
# from uuid import UUID, uuid4
# from motor.motor_asyncio import AsyncIOMotorClient
#
# from pydantic import Field
# from beanie import Document, Indexed, init_beanie
#
# from config import MONGO_URL
#
#
# class Product(Document):
#     id: UUID = Field(default_factory=uuid4)
#     name: str
#     description: Optional[str] = None
#     main_image_url: Optional[str]
#     image1_url: Optional[str]
#     image2_url: Optional[str]
#     image3_url: Optional[str]
#     image4_url: Optional[str]
#     image5_url: Optional[str]
#     price: Indexed(float)
#
#     class Settings:
#         name = "product"
#
#
# async def init():
#     client = AsyncIOMotorClient(MONGO_URL)
#
#     await init_beanie(database=client.db_name, document_models=[Product])
#
# asyncio.run(init())

from pymongo.mongo_client import MongoClient

from config import MONGO_URL

db = MongoClient(MONGO_URL,
                 tls=True,
                 tlsAllowInvalidCertificates=True)
findaz_db = db.findazdb
