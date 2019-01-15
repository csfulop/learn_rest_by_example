from db.adapter import PhonebookDbAdapter, Entry, PhonebookDbException


class MemoryPhonebookDbAdapter(PhonebookDbAdapter):
    _phonebook = {}

    def size(self):
        return len(self._phonebook)

    def add(self, entry: Entry):
        if not entry.id:
            raise PhonebookDbException("missing id for entry: " + str(entry))
        self._phonebook[entry.id] = entry

    def remove(self, entry: Entry):
        pass

    def get(self, id):
        pass

    def list(self):
        pass
