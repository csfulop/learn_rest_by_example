from abc import ABC, abstractmethod

from src.main.db.entry import Entry


class PhonebookAdapter(ABC):

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