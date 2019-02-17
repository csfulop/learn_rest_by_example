from typing import List

from pecan import expose, abort, request
from pecan.rest import RestController

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry, PhonebookDbException
from restbyexample.phonebook.pecan.controllers.phonebook_entry_controller import PhonebookEntryController


class PhonebookController(RestController):
    """
    Pecan controller object to handle requests for the root of the Phonebook.
    Extend the RestController of Pecan to implement the Phonebook RESTful API.
    For more details see: https://pecan.readthedocs.io/en/latest/rest.html#writing-restful-web-services-with-restcontroller
    """

    def __init__(self, db_adapter: PhonebookDbAdapter) -> None:
        super().__init__()
        self._db_adapter = db_adapter

    @expose()
    def _lookup(self, entry_id: str, *remainder):
        """
        If there are remaining path elements in the URL then process the request with a PhonebookEntryController
        :param entry_id: the ID of the requested Entry
        :param remainder: any remainging path elements of the URL
        :return: controller for the given Entry
        """
        return PhonebookEntryController(self._db_adapter, entry_id), remainder

    @expose(template='json')
    def get_all(self) -> List[Entry]:
        """
        List all Phonebook Entries
        :return: list of all Phonebook Entries
        """
        return self._db_adapter.list()

    @expose(template='json')
    def post(self) -> Entry:
        """
        Create new Phonebook Entry.
        The content of the Entry will be set from the JSON request body.
        :return: the created Phonebook Entry
        """
        entry = Entry(**request.json)
        try:
            self._db_adapter.add(entry)
        except PhonebookDbException as e:
            abort(400, e.args[0])
        return entry
