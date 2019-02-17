from copy import deepcopy
from typing import Optional, List
from uuid import uuid4

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry, PhonebookDbException


class MemoryPhonebookDbAdapter(PhonebookDbAdapter):
    """
    Simple PhonebookDbAdapter implementation to store the Phonebook data in a in-memory dict.
    """

    def __init__(self) -> None:
        super().__init__()
        self._phonebook = {}

    def size(self) -> int:
        return len(self._phonebook)

    def add(self, entry: Entry) -> None:
        if not entry.id:
            entry.id = str(uuid4())
        if entry.id in self._phonebook:
            raise PhonebookDbException('ID already exists: ' + str(entry.id))
        self._phonebook[entry.id] = deepcopy(entry)

    def remove(self, entry_id: str) -> None:
        if entry_id in self._phonebook:
            del self._phonebook[entry_id]
        else:
            raise PhonebookDbException('Entry with the given ID does not exists: ' + str(entry_id))

    def get(self, entry_id: str) -> Optional[Entry]:
        if entry_id in self._phonebook:
            return deepcopy(self._phonebook[entry_id])
        else:
            return None

    def modify(self, entry: Entry) -> None:
        if not entry.id:
            raise PhonebookDbException('Can not modify Entry without ID')
        if entry.id not in self._phonebook:
            raise PhonebookDbException('Entry does not exists with ID: ' + str(entry.id))
        self._phonebook[entry.id] = deepcopy(entry)

    def list(self) -> List[Entry]:
        return deepcopy(list(self._phonebook.values()))
