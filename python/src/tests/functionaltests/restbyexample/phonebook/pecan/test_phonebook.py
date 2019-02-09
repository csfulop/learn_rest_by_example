from hamcrest import empty, has_length, has_item, equal_to
from hamcrest.core import assert_that
from hamcrest.core.core import is_

from functionaltests.restbyexample.phonebook.matchers import json_equal_to_entry
from functionaltests.restbyexample.phonebook.pecan.functional_test_base import FunctionalTestBase
from restbyexample.phonebook.db.adapter import Entry
from restbyexample.phonebook.pecan.utils import objToDict

HTTP_404 = 'The resource could not be found.'
HTTP_405 = 'The server could not comply with the request since it is either malformed or otherwise incorrect.'


class TestPhonebook(FunctionalTestBase):
    def test_get_list_of_empty_phonebook_should_return_empty_list(self):
        # when
        response = self.app.get('/phonebook')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, equal_to([]))

    def test_get_list_with_trailing_slash(self):
        # when
        response = self.app.get('/phonebook/')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, equal_to([]))

    def test_get_invalid_url_should_fail(self):
        # when
        response = self.app.get('/bogus/url', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        assert_that(response.json, equal_to({'status': 404, 'detail': HTTP_404}))

    def test_post_entry_without_id_should_generate_random_id(self):
        # when
        response = self.app.post_json('/phonebook/', params={'name': 'Alice', 'phone': '1234'})
        # then
        assert_that(response.status_int, is_(200))
        entry_id = response.json['id']
        expected = Entry(entry_id, name='Alice', phone='1234')
        assert_that(response.json, json_equal_to_entry(expected))
        get_result = self.app.get('/phonebook/' + entry_id).json
        assert_that(get_result, json_equal_to_entry(expected))

    def test_post_entry_should_save_entry(self):
        # given
        entry = Entry('1234')
        # when
        response = self.app.post_json(url='/phonebook', params=objToDict(entry))
        # then
        assert_that(response.status_int, is_(200))
        assert_that(self.app.get(url='/phonebook/').json, has_length(1))

    def test_post_entry_with_trailing_slash(self):
        # given
        entry = Entry('1234')
        # when
        response = self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # then
        assert_that(response.status_int, is_(200))
        assert_that(self.app.get(url='/phonebook/').json, has_length(1))

    def test_post_same_id_twice_should_fail(self):
        # given
        entry1 = Entry('1234')
        entry2 = Entry('1234')
        # when
        self.app.post_json(url='/phonebook/', params=objToDict(entry1))
        response = self.app.post_json(url='/phonebook/', params=objToDict(entry2), expect_errors=True)
        # then
        assert_that(response.status_int, is_(400))
        assert_that(response.json, equal_to({'status': 400, 'detail': 'ID already exists: 1234'}))

    def test_post_to_subresource_should_fail(self):
        # given
        entry = Entry('1234')
        # when
        response = self.app.post_json(url='/phonebook/asdf', params=objToDict(entry), expect_errors=True)
        # then
        assert_that(response.status_int, is_(405))
        assert_that(response.json, equal_to({'status': 405, 'detail': HTTP_405}))

    def test_get_entry_by_id_with_trailing_slash(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.get('/phonebook/1234/')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(entry))

    def test_get_entry_by_id(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.get('/phonebook/1234')
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(entry))

    def test_get_subresource_of_entry_should_fail(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.get('/phonebook/1234/asdf', expect_errors=True)
        # then
        assert_that(response.status_int, is_(405))
        assert_that(response.json, equal_to({'status': 405, 'detail': HTTP_405}))

    def test_get_should_fail_if_no_entry_found(self):
        # when
        response = self.app.get('/phonebook/asdf/', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        assert_that(response.json, equal_to({'status': 404, 'detail': HTTP_404}))

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
        assert_that(self.app.get('/phonebook/1234/', expect_errors=True).status_int, is_(404))
        assert_that(self.app.get('/phonebook/').json, empty())

    def test_delete_entry_with_trailing_slash(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.delete(url='/phonebook/1234/')
        # then
        assert_that(response.status_int, is_(204))
        assert_that(self.app.get('/phonebook/').json, empty())

    def test_delete_nonexisting_entry_should_fail(self):
        # when
        response = self.app.delete(url='/phonebook/1234', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        assert_that(response.json, equal_to({'status': 404, 'detail': 'Entry with the given ID does not exists: 1234'}))

    def test_delete_subresource_should_fail(self):
        # given
        entry = Entry('1234', name='Charlie')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.delete(url='/phonebook/1234/asdf', expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        assert_that(response.json, equal_to({'status': 404, 'detail': HTTP_404}))

    def test_put_should_modify_whole_entry(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        entry2 = Entry('1234', name='Bob', mobile='9876')
        response = self.app.put_json(url='/phonebook/1234', params=objToDict(entry2))
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(entry2))
        assert_that(self.app.get(url='/phonebook/1234').json, json_equal_to_entry(entry2))

    def test_put_without_id(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        entry2 = Entry(name='Bob', mobile='9876')
        response = self.app.put_json(url='/phonebook/1234', params=objToDict(entry2))
        # then
        expected = Entry('1234', name='Bob', mobile='9876')
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(expected))
        assert_that(self.app.get(url='/phonebook/1234').json, json_equal_to_entry(expected))

    def test_put_should_fail_when_id_in_url_and_body_mismatch(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        entry2 = Entry('4567', name='Bob', mobile='9876')
        response = self.app.put_json(url='/phonebook/1234', params=objToDict(entry2), expect_errors=True)
        # then
        assert_that(response.status_int, is_(400))
        assert_that(response.json, equal_to({'status': 400, 'detail': 'Entry ID in URL and body mismatch'}))

    def test_put_new_entry_id_only_in_url(self):
        # given
        entry = Entry(name='Charlie', phone='5678')
        # when
        response = self.app.put_json(url='/phonebook/1234', params=objToDict(entry))
        # then
        expected = Entry('1234', name='Charlie', phone='5678')
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(expected))
        assert_that(self.app.get(url='/phonebook/1234').json, json_equal_to_entry(expected))

    def test_put_new_entry_id_in_url_and_body(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        # when
        response = self.app.put_json(url='/phonebook/1234', params=objToDict(entry))
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(entry))
        assert_that(self.app.get(url='/phonebook/1234').json, json_equal_to_entry(entry))

    def test_put_with_trailing_slash(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        # when
        response = self.app.put_json(url='/phonebook/1234/', params=objToDict(entry))
        # then
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(entry))
        assert_that(self.app.get(url='/phonebook/1234').json, json_equal_to_entry(entry))

    def test_put_to_subresource_should_fail(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        # when
        response = self.app.put_json(url='/phonebook/1234/asdf', params=objToDict(entry), expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        assert_that(response.json, equal_to({'status': 404, 'detail': HTTP_404}))

    def test_patch(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.patch_json(url='/phonebook/1234', params={'name': 'David', 'phone': None, 'mobile': 5555})
        # then
        expected = Entry('1234', name='David', mobile=5555)
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(expected))
        assert_that(self.app.get(url='/phonebook/1234').json, json_equal_to_entry(expected))

    def test_patch_with_trailing_slash(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.patch_json(url='/phonebook/1234/', params={'name': 'David', 'phone': None, 'mobile': 5555})
        # then
        expected = Entry('1234', name='David', mobile=5555)
        assert_that(response.status_int, is_(200))
        assert_that(response.json, json_equal_to_entry(expected))
        assert_that(self.app.get(url='/phonebook/1234').json, json_equal_to_entry(expected))

    def test_patch_non_existing_entry_should_fail(self):
        # when
        response = self.app.patch_json(url='/phonebook/1234',
                                       params={'name': 'David', 'phone': None, 'mobile': 5555},
                                       expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        assert_that(response.json, equal_to({'status': 404, 'detail': 'Entry does not exists with ID: 1234'}))

    def test_patch_should_fail_when_id_in_url_and_body_mismatch(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.patch_json(url='/phonebook/1234', params={'id': '456', 'name': 'David'}, expect_errors=True)
        # then
        assert_that(response.status_int, is_(400))
        assert_that(response.json, equal_to({'status': 400, 'detail': 'Entry ID in URL and body mismatch'}))

    def test_patch_to_subresource_should_fail(self):
        # given
        entry = Entry('1234', name='Charlie', phone='5678')
        self.app.post_json(url='/phonebook/', params=objToDict(entry))
        # when
        response = self.app.patch_json(url='/phonebook/1234/asdf',
                                       params={'name': 'David', 'phone': None, 'mobile': 5555},
                                       expect_errors=True)
        # then
        assert_that(response.status_int, is_(404))
        assert_that(response.json, equal_to({'status': 404, 'detail': HTTP_404}))

    def test_base_url_should_reject_put(self):
        # given
        entry = Entry(name='Charlie', phone='5678')
        # when
        response = self.app.put_json(url='/phonebook/', params=objToDict(entry), expect_errors=True)
        # then
        assert_that(response.status_int, is_(405))
        assert_that(response.json, equal_to({'status': 405, 'detail': HTTP_405}))

    def test_base_url_should_reject_patch(self):
        # given
        entry = Entry(name='Charlie', phone='5678')
        # when
        response = self.app.patch_json(url='/phonebook/', params=objToDict(entry), expect_errors=True)
        # then
        assert_that(response.status_int, is_(405))
        assert_that(response.json, equal_to({'status': 405, 'detail': HTTP_405}))

    def test_base_url_should_reject_delete(self):
        # when
        response = self.app.delete(url='/phonebook/', expect_errors=True)
        # then
        assert_that(response.status_int, is_(405))
        assert_that(response.json, equal_to({'status': 405, 'detail': HTTP_405}))

    def test_entry_should_reject_post(self):
        # given
        entry = Entry(name='Charlie', phone='5678')
        # when
        response = self.app.post_json(url='/phonebook/1234', params=objToDict(entry), expect_errors=True)
        # then
        assert_that(response.status_int, is_(405))
        assert_that(response.json, equal_to({'status': 405, 'detail': HTTP_405}))
