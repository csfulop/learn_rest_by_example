from uuid import uuid4

from db.adapter import PhonebookDbAdapter, Entry, PhonebookDbException


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
            entry.id = uuid4()
        self._phonebook[entry.id] = entry

    def remove(self, entry: Entry):
        pass

    def get(self, id) -> Entry:
        return self._phonebook[id]

    def list(self):
        pass
