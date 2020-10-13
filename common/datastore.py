from abc import ABCMeta, abstractmethod
from typing import Dict


class DataStore(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'insert') and
                callable(subclass.insert) and
                hasattr(subclass, 'find_one') and
                callable(subclass.find_one) and
                hasattr(subclass, 'update') and
                callable(subclass.update) and
                hasattr(subclass, 'remove') and
                callable(subclass.remove) and
                hasattr(subclass, 'find') and
                callable(subclass.find) or
                NotImplemented)

    @staticmethod
    @abstractmethod
    def insert(collection: str, data: Dict):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def find(collection: str, query: Dict):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def find_one(collection: str, query: Dict) -> Dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def remove(collection: str, query: Dict) -> None:
        raise NotImplementedError
