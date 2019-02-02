import pecan
from pecan import expose
from pecan.rest import RestController

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry


class PhonebookController(RestController):

    def __init__(self, db_adapter: PhonebookDbAdapter) -> None:
        super().__init__()
        self._db_adapter = db_adapter

    @expose(template='json')
    def get_all(self):
        return [objToDict(e) for e in self._db_adapter.list()]

    @expose(template='json')
    def get_one(self, id_: str):
        result = self._db_adapter.get(id_)
        if result is None:
            pecan.response.status = 404
        else:
            return objToDict(result)

    @expose(template='json')
    def post(self, **kw):
        entity = Entry(**kw)
        self._db_adapter.add(entity)
        return objToDict(entity)

    @expose(template='json')
    def put(self, id_: str, **kw):
        entity = Entry(**kw)
        self._db_adapter.modify(entity)

    @expose(template='json')
    def delete(self, id_: str):
        if self._db_adapter.get(id_):
            self._db_adapter.remove(id_)
            pecan.response.status = 204
        else:
            pecan.response.status = 404


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
