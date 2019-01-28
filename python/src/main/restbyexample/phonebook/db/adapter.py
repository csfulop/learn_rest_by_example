from abc import ABC, abstractmethod
from typing import Optional, Collection


class Entry:
    def __init__(self, id: str = None, **kwargs) -> None:
        self.id = id
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PhonebookDbAdapter(ABC):

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def add(self, entry: Entry) -> None:
        pass

    @abstractmethod
    def remove(self, id) -> None:
        pass

    @abstractmethod
    def get(self, id) -> Optional[Entry]:
        pass

    @abstractmethod
    def list(self) -> Collection[Entry]:
        pass


class PhonebookDbException(Exception):
    pass
