from pecan import abort, expose

# Note: this is *not* thread-safe.  In real life, use a persistent data store.
from pecan.rest import RestController

from restbyexample.phonebook import PhonebookDbAdapterImpl
from restbyexample.phonebook.pecan.controllers.phonebook_controller import PhonebookController

BOOKS = {
    '0': 'The Last of the Mohicans',
    '1': 'Catch-22'
}


class RootController(object):
    phonebook = PhonebookController(PhonebookDbAdapterImpl())
