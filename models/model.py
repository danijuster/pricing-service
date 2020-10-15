from typing import List, TypeVar, Type, Dict, Union
from abc import ABCMeta, abstractmethod
from common.datastore import DataStore

T = TypeVar("T", bound="Model")


class Model(metaclass=ABCMeta):
    collection: str
    _id: str
    datastore: DataStore
    datastore_name: str

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def initialize(cls: Type[T], datastore: DataStore):
        cls.datastore = datastore
        cls.datastore_name = repr(cls.datastore).split('.')[-1][:-2]

    def save_to_mongo(self):
        self.datastore.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        self.datastore.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by('_id', _id)

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = cls.datastore.find(cls.collection, {})
        return [cls(**element) for element in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:
        return cls(**cls.datastore.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> List[T]:
        return [cls(**element) for element in cls.datastore.find(cls.collection, {attribute: value})]
