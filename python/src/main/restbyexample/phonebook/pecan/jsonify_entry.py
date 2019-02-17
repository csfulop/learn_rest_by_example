"""
Use JSON serialization support of Pecan to convert Entry objects to JSON documents.
For more details see: https://pecan.readthedocs.io/en/latest/jsonify.html
"""

from pecan.jsonify import jsonify

from restbyexample.phonebook.db.adapter import Entry
from restbyexample.phonebook.pecan.utils import objToDict


def register_jsonify():
    """dummy function to avoid import organizer to remove the 'empty' import of this module."""
    pass


@jsonify.register(Entry)
def jsonify_entry(entry: Entry):
    return objToDict(entry)
