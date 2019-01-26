from hamcrest import empty, has_key
from hamcrest.core import assert_that
from hamcrest.core.core import is_

from functionaltests.restbyexample.phonebook.pecan.functional_test_base import FunctionalTestBase


class TestPhonebook(FunctionalTestBase):
    def test_list(self):
        response = self.app.get('/phonebook/')
        assert_that(response.status_int, is_(200))
        assert_that(response.json, empty())

    def test_get_not_found(self):
        response = self.app.get('/a/bogus/url', expect_errors=True)
        assert response.status_int == 404

    def test_add_entry(self):
        response = self.app.post_json('/phonebook/', params={'name': 'Alice', 'phone': '1234'})
        assert_that(response.status_int, is_(200))
        assert_that(response.json, has_key('id'))
