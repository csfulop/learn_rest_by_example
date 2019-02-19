"""
The built in simple server of Pecan (pecan serve) is not recommended for production.
Use cheroot in production.
For more details see: https://pecan.readthedocs.io/en/latest/deployment.html
"""

import os
from threading import Thread

from cheroot import wsgi
from pecan.deploy import deploy

phonebook_wsgi_app = deploy(os.path.join(os.path.dirname(__file__), 'config.py'))

server = wsgi.Server(('0.0.0.0', 8080), phonebook_wsgi_app)

t = Thread(target=server.start)
print("Starting server...")
t.start()
input("Press Enter to continue...")
print("Terminating server...")
server.stop()
