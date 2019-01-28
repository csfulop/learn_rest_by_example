from pecan import expose

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry


class PhonebookController(object):
    def __init__(self, db_adapter: PhonebookDbAdapter) -> None:
        super().__init__()
        self._db_adapter = db_adapter

    @expose()
    def _lookup(self, id_, *remainder):
        return PhonebookEntryController(id_, self._db_adapter), remainder

    @expose(generic=True, template='json')
    def index(self):
        return [objToDict(e) for e in self._db_adapter.list()]

    @index.when(method='POST', template='json')
    def index_POST(self, **kw):
        entity = Entry(**kw)
        self._db_adapter.add(entity)
        return objToDict(entity)


# FIXME: this requires trailing slash, make it work without trailing slash
class PhonebookEntryController(object):

    def __init__(self, id_, db_adapter: PhonebookDbAdapter) -> None:
        super().__init__()
        self._id = id_
        self._db_adapter = db_adapter

    @expose(generic=True, template='json')
    def index(self):
        return objToDict(self._db_adapter.get(self._id))


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
