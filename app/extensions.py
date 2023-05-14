from pymongo.mongo_client import MongoClient

from config import MONGO_URL

db = MongoClient(MONGO_URL,
                 tls=True,
                 tlsAllowInvalidCertificates=True)
findaz_db = db.findazdb
