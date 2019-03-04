from unittest import TestCase

import requests
from hamcrest.core import assert_that
from hamcrest.core.core import is_

BASE_URL = 'http://localhost:8080/'


class TestBlackBoxPhonebook(TestCase):
    def test_empty_phonebook(self):
        # given
        # when
        response = requests.get(BASE_URL + 'phonebook/')
        # then
        assert_that(response.status_code, is_(200))
        assert_that(response.json(), is_([]))
