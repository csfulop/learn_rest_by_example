# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'restbyexample.phonebook.pecan.controllers.root.RootController',
    'modules': ['restbyexample.phonebook.pecan'],
    'static_root': '%(confdir)s/../../../../../main/restbyexample/phonebook/pecan/public',
    'template_path': '%(confdir)s/../../../../../src/main/restbyexample/phonebook/pecan/templates',
    'debug': True,
    'errors': {
        '404': '/error/404',
        '__force_dict__': True
    }
}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
