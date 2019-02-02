from hamcrest import empty, has_length, has_item, equal_to
from hamcrest.core import assert_that
from hamcrest.core.core import is_

from functionaltests.restbyexample.phonebook.pecan.functional_test_base import FunctionalTestBase
from restbyexample.phonebook.db.adapter import Entry
from restbyexample.phonebook.pecan.controllers.phonebook_controller import objToDict


class TestPhonebook(FunctionalTestBase):
    def test_get_list_of_empty_phonebook_should_return_empty_list(self):
        # when
        response = self.app.get('/phonebook/')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, empty())

    # FIXME: test invalid method

    def test_get_invalid_url_should_fail(self):
        # when
        response = self.app.get('/phonebook/bogus/url', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))

    def test_post_entry_without_id_should_generate_random_id(self):
        # when
        response = self.app.post_json('/phonebook/', params={'name': 'Alice', 'phone': '1234'})
        # then
        assert_that(response.status_int, is_(200))
        id_ = response.json['id']
        get_result = self.app.get('/phonebook/' + id_ + '/').json
        assert_that(get_result, is_({'id': id_, 'name': 'Alice', 'phone': '1234'}))

    def test_post_entry_should_save_entry(self):
        # given
        entry = Entry('1234')
        # when
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # then
        assert_that(self.app.get(url='/phonebook/').json, has_length(1))

    def test_post_same_id_twice_should_fail(self):
        # given
        entry1 = Entry('1234')
        entry2 = Entry('1234')
        # when
        self.app.post_json(url='/phonebook/', params=objToDict(entry1))
        response = self.app.post_json(url='/phonebook/', params=objToDict(entry2), expect_errors=True)
        # then
        assert_that(response.status_int, is_(500))  # FIXME: should use correct status code
        # FIXME: should return json error content

    def test_get_entry_by_id_with_trailing_slash(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.get('/phonebook/1234/')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, is_(objToDict(entry)))

    def test_get_entry_by_id(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.get('/phonebook/1234')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, is_(objToDict(entry)))

    def test_get_subresource_of_entry_should_send_404(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.get('/phonebook/1234/asdf', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))

    def test_get_should_return_404_if_no_entry_found(self):
        # when
        response = self.app.get('/phonebook/asdf/', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        # FIXME: assert error message

    def test_get_list_of_multiple_entries(self):
        # given
        self.app.post_json('/phonebook/', params={'name': 'Alice', 'id': '1'})
        self.app.post_json('/phonebook/', params={'name': 'Bob', 'id': '2'})
        # when
        response = self.app.get('/phonebook')
        # then
        list = response.json
        assert_that(list, has_length(2))
        assert_that(list, has_item({'name': 'Alice', 'id': '1'}))
        assert_that(list, has_item({'name': 'Bob', 'id': '2'}))

    def test_delete_entry(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.delete(url='/phonebook/1234')
        # then
        assert_that(response.status_int, is_(204))
        response = self.app.get('/phonebook/1234/', expect_errors=True)
        assert_that(response.status_int, is_(404))
        response = self.app.get('/phonebook/')
        assert_that(response.json, empty())

    def test_delete_nonexisting_entry_should_fail(self):
        # when
        response = self.app.delete(url='/phonebook/1234', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))

    def test_put_should_modify_whole_entry(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        entry2 = Entry('1234', name='Bob', mobile='9876')
        self.app.put_json(url='/phonebook/1234', params=objToDict(entry2))
        # then
        assert_that(self.app.get(url='/phonebook/1234').json, equal_to(objToDict(entry2)))
