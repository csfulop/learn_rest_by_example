from copy import deepcopy
from typing import Optional, Collection
from uuid import uuid4

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry, PhonebookDbException


class MemoryPhonebookDbAdapter(PhonebookDbAdapter):
    def __init__(self) -> None:
        super().__init__()
        self._phonebook = {}

    def size(self) -> int:
        return len(self._phonebook)

    def add(self, entry: Entry) -> None:
        if entry.id in self._phonebook:
            raise PhonebookDbException("id already exists: " + str(entry.id))
        if not entry.id:
            entry.id = str(uuid4())
        self._phonebook[entry.id] = deepcopy(entry)

    def remove(self, id_) -> None:
        if id_ in self._phonebook:
            del self._phonebook[id_]
        else:
            raise PhonebookDbException("Entry with the given id does not exists: " + str(id_))

    def get(self, id_) -> Optional[Entry]:
        if id_ in self._phonebook:
            return deepcopy(self._phonebook[id_])
        else:
            return None

    def list(self) -> Collection[Entry]:
        return deepcopy(list(self._phonebook.values()))
