import os

from cheroot import wsgi
from pecan.deploy import deploy

phonebook_wsgi_app = deploy(os.path.join(os.path.dirname(__file__), 'config.py'))

server = wsgi.Server(('0.0.0.0', 8080), phonebook_wsgi_app)

try:
    server.start()
except KeyboardInterrupt:
    print("Terminating server...")
    server.stop()
