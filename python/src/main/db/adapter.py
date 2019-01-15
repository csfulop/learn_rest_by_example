from abc import ABC, abstractmethod


class Entry:
    id = None


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
