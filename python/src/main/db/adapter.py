from abc import ABC, abstractmethod


class Entry:
    id = None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class PhonebookDbAdapter(ABC):

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def add(self, entry: Entry):
        pass

    @abstractmethod
    def remove(self, entry: Entry):
        pass

    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def list(self):
        pass


class PhonebookDbException(Exception):
    pass
