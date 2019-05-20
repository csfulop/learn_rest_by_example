from threading import Thread
from unittest import TestCase, skip

import requests
from hamcrest.core import assert_that
from hamcrest.core.core import is_
from requests import ConnectionError

from restbyexample.phonebook.pecan.run_cheroot import run, main


class TestRunCheroot(TestCase):
    def test_run_cheroot(self):
        # given
        self.addCleanup(main.stop)
        t = Thread(target=run)
        # when
        t.start()
        # then
        response = requests.get(url='http://localhost:8080/phonebook/')
        assert_that(response.status_code, is_(200))
        assert_that(response.json(), is_([]))
        # when
        main.stop()
        # then
        with self.assertRaises(ConnectionError):
            requests.get(url='http://localhost:8080/phonebook/')
