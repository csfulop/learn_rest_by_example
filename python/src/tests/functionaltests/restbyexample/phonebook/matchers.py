from hamcrest.core.core.isequal import IsEqual

from restbyexample.phonebook.db.adapter import Entry
from restbyexample.phonebook.pecan.utils import objToDict


class JsonEqualToEntry(IsEqual):
    def __init__(self, entry: Entry) -> None:
        super().__init__(objToDict(entry))


def json_equal_to_entry(entry: Entry):
    return JsonEqualToEntry(entry)
