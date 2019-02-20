"""
The built in simple server of Pecan (pecan serve) is not recommended for production.
Use cheroot in production.
For more details see: https://pecan.readthedocs.io/en/latest/deployment.html
"""

import os

from cheroot import wsgi
from pecan.deploy import deploy


class Main:

    def __init__(self) -> None:
        super().__init__()
        self._phonebook_wsgi_app = deploy(os.path.join(os.path.dirname(__file__), 'config.py'))
        self._server = wsgi.Server(('0.0.0.0', 8080), self._phonebook_wsgi_app)

    def start(self):
        self._server.start()

    def stop(self):
        self._server.stop()


main = Main()


def run():
    try:
        print("Starting server...")
        main.start()
    except KeyboardInterrupt:
        print("Terminating server...")
        main.stop()


if __name__ == "__main__":
    run()
