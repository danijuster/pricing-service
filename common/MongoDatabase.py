from typing import Dict
import pymongo
from common.datastore import DataStore


class MongoDatabase(DataStore):
    URI = "mongodb://127.0.0.1:27017/pricing"
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert(collection: str, data: Dict):
        """Overrides DataStore.insert()"""
        MongoDatabase.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        """Overrides DataStore.find()"""
        return MongoDatabase.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        """Overrides DataStore.find_one()"""
        return MongoDatabase.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        """Overrides DataStore.update()"""
        MongoDatabase.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> None:
        """Overrides DataStore.remove()"""
        MongoDatabase.DATABASE[collection].remove(query)
