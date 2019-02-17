from abc import ABC, abstractmethod
from typing import Optional, List


class Entry:
    def __init__(self, id: str = None, **kwargs) -> None:
        self.id = id
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PhonebookDbAdapter(ABC):
    """
    Abstract Adapter class to access some Database.
    It should hide every Database related stuff.
    """

    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def add(self, entry: Entry) -> None:
        pass

    @abstractmethod
    def remove(self, id: str) -> None:
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[Entry]:
        pass

    @abstractmethod
    def modify(self, entry: Entry):
        pass

    @abstractmethod
    def list(self) -> List[Entry]:
        pass


class PhonebookDbException(Exception):
    pass
