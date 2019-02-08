from pecan import make_app
from restbyexample.phonebook.pecan import model
from restbyexample.phonebook.pecan.controllers.json_error_hook import JsonErrorHook


def setup_app(config):

    model.init_model()
    app_conf = dict(config.app)

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=[JsonErrorHook()],
        **app_conf
    )
