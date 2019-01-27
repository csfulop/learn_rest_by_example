from pecan import expose

from restbyexample.phonebook.db.adapter import PhonebookDbAdapter, Entry


class PhonebookController(object):
    def __init__(self, db_adapter: PhonebookDbAdapter) -> None:
        super().__init__()
        self.db_adapter = db_adapter

    @expose(generic=True, template='json')
    def index(self):
        return [e.__dict__ for e in self.db_adapter.list()]  # FIXME: use JSONEncoder

    @index.when(method='POST', template='json')
    def index_POST(self, **kw):
        entity = Entry(**kw)
        self.db_adapter.add(entity)
        return entity.__dict__  # FIXME: use JSONEncoder
