import json_merge_patch
import pecan
from pecan import expose, abort, request
from pecan.rest import RestController

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry, PhonebookDbException


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


class PhonebookEntryController(RestController):

    def __init__(self, db_adapter: PhonebookDbAdapter, entry_id: str) -> None:
        super().__init__()
        self._db_adapter = db_adapter
        self._entry_id = entry_id

    @expose(template='json')
    def get_all(self):
        result = self._db_adapter.get(self._entry_id)
        if result is None:
            abort(404)
        else:
            return objToDict(result)

    @expose(template='json')
    def put(self):
        modified_entry = request.json
        entry_id = modified_entry.pop('id', None)
        if not entry_id:
            entry_id = self._entry_id
        elif entry_id != self._entry_id:
            abort(400, detail='Entry ID in URL and body mismatch')
        entry = Entry(entry_id, **modified_entry)
        if self._db_adapter.get(entry_id):  # FIXME: add exists to adapter
            self._db_adapter.modify(entry)
        else:
            self._db_adapter.add(entry)
        return objToDict(entry)

    @expose(template='json')
    def patch(self):
        actual = objToDict(self._db_adapter.get(self._entry_id))
        if actual is None:
            abort(404, detail='Entry does not exists with ID: ' + self._entry_id)
        patch = request.json
        if 'id' in patch and patch['id'] != self._entry_id:
            abort(400, detail='Entry ID in URL and body mismatch')
        result = json_merge_patch.merge(actual, patch)
        result.pop('id')
        self._db_adapter.modify(Entry(self._entry_id, **result))
        return objToDict(self._db_adapter.get(self._entry_id))

    @expose(template='json')
    def delete(self):
        try:
            self._db_adapter.remove(self._entry_id)
            pecan.response.status = 204
        except PhonebookDbException as e:
            abort(404, e.args[0])


def objToDict(obj):
    """
    Convert Entry (or any other object) to dict, because object by default is not JSON serializable, but dict is.
    Instead of changing the business object to match with the requirements of the REST layer,
    the REST layer should make the necessary API <--> business logic transformations.
    (it should be possible to provide different APIs with conflicting requirements for the same business logic)
    :param obj: object to be converted
    :return: dict representation of the data
    """
    if isinstance(obj, object) and hasattr(obj, '__dict__'):
        result = obj.__dict__
    else:
        result = obj

    if isinstance(result, dict):
        result = {key: objToDict(value) for key, value in result.items()}

    if isinstance(result, list):
        result = [objToDict(o) for o in result]

    if isinstance(result, tuple):
        result = tuple(objToDict(o) for o in result)

    return result
