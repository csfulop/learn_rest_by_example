from db.adapter import PhonebookAdapter
from db.entry import Entry


class MemoryPhonebookAdapter(PhonebookAdapter):

    def add(self, entry: Entry):
        pass

    def remove(self, entry: Entry):
        pass

    def get(self, id):
        pass

    def list(self):
        pass
