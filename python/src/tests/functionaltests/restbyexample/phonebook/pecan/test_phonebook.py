from hamcrest import empty, has_key, has_length
from hamcrest.core import assert_that
from hamcrest.core.core import is_

from functionaltests.restbyexample.phonebook.pecan.functional_test_base import FunctionalTestBase
from restbyexample.phonebook.db.adapter import Entry


class TestPhonebook(FunctionalTestBase):
    def test_list_of_empty_phonebook_should_return_empty_list(self):
        # when
        response = self.app.get('/phonebook/')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, empty())

    # FIXME: test invalid method

    def test_get_not_found(self):
        # when
        response = self.app.get('/phonebook/bogus/url', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))

    def test_add_entry_without_id_should_generate_random_id(self):
        # when
        response = self.app.post_json('/phonebook/', params={'name': 'Alice', 'phone': '1234'})
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, has_key('id'))

    def test_add_entry_should_save_entry(self):
        # given
        entry = Entry(1234)
        # when
        self.app.post_json(url='/phonebook/', params=entry.__dict__)  # FIXME: use JSONEncoder
        # then
        assert_that(self.app.get(url='/phonebook/').json, has_length(1))
