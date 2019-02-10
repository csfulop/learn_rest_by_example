from pecan.jsonify import jsonify

from restbyexample.phonebook.db.adapter import Entry
from restbyexample.phonebook.pecan.utils import objToDict


def register_jsonify():
    pass


@jsonify.register(Entry)
def jsonify_entry(entry: Entry):
    return objToDict(entry)
