"""
The built in simple server of Pecan (pecan serve) is not recommended for production.
Use cheroot in production.
For more details see: https://pecan.readthedocs.io/en/latest/deployment.html
"""

import os

from cheroot import wsgi
from pecan.deploy import deploy

phonebook_wsgi_app = deploy(os.path.join(os.path.dirname(__file__), 'config.py'))

server = wsgi.Server(('0.0.0.0', 8080), phonebook_wsgi_app)

try:
    print("Starting server...")
    server.start()
except KeyboardInterrupt:
    print("Terminating server...")
    server.stop()
