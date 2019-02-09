from pecan import expose, abort, request
from pecan.rest import RestController

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry, PhonebookDbException
from restbyexample.phonebook.pecan.controllers.phonebook_entry_controller import PhonebookEntryController
from restbyexample.phonebook.pecan.utils import objToDict


class PhonebookController(RestController):
    def __init__(self, db_adapter: PhonebookDbAdapter) -> None:
        super().__init__()
        self._db_adapter = db_adapter

    @expose()
    def _lookup(self, entry_id, *remainder):
        if entry_id is not None:
            return PhonebookEntryController(self._db_adapter, entry_id), remainder
        abort(404)

    @expose(template='json')
    def get_all(self):
        return [objToDict(e) for e in self._db_adapter.list()]

    @expose(template='json')
    def post(self):
        entry = Entry(**request.json)
        try:
            self._db_adapter.add(entry)
        except PhonebookDbException as e:
            abort(400, e.args[0])
        return objToDict(entry)
