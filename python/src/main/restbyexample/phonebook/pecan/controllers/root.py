from restbyexample.phonebook.di import PhonebookDbAdapterImpl
from restbyexample.phonebook.pecan.controllers.phonebook_controller import PhonebookController


class RootController(object):
    phonebook = PhonebookController(PhonebookDbAdapterImpl())
