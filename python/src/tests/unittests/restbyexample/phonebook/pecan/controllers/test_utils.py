from unittest import TestCase

from hamcrest.core import assert_that
from hamcrest.core.core import is_

from restbyexample.phonebook.db.adapter import Entry
from restbyexample.phonebook.pecan.controllers.utils import objToDict


class TestObjToDict(TestCase):

    def test_obj_to_dict_with_builtin_types(self):
        assert_that(objToDict(1), is_(1))
        assert_that(objToDict(1.2), is_(1.2))
        assert_that(objToDict(True), is_(True))
        assert_that(objToDict("asdf"), is_("asdf"))
        assert_that(objToDict(None), is_(None))
        assert_that(objToDict([1, 2, 3]), is_([1, 2, 3]))
        assert_that(objToDict((1, 2, 3)), is_((1, 2, 3)))
        assert_that(objToDict({1, 2, 3}), is_({1, 2, 3}))  # FIXME: set is not JSON serializable
        assert_that(objToDict({'a': 1, 'b': 2}), is_({'a': 1, 'b': 2}))

    def test_obj_to_dict(self):
        # given
        e = Entry('1234', name='Alice')
        # when
        result = objToDict(e)
        # then
        assert_that(result, is_({'id': '1234', 'name': 'Alice'}))

    def test_obj_to_dict_with_object_in_object(self):
        # given
        e1 = Entry('1234', name='Alice')
        e2 = Entry('456', parent=e1)
        # when
        result = objToDict(e2)
        # then
        assert_that(result, is_({'id': '456', 'parent': {'id': '1234', 'name': 'Alice'}}))

    def test_obj_to_dict_with_object_in_list(self):
        # given
        e1 = Entry('1234', name='Alice')
        e2 = Entry('456')
        # when
        result = objToDict([e1, e2])
        # then
        assert_that(result, is_([{'id': '1234', 'name': 'Alice'}, {'id': '456'}]))

    def test_obj_to_dict_with_object_in_tuple(self):
        # given
        e1 = Entry('1234', name='Alice')
        e2 = Entry('456')
        # when
        result = objToDict((e1, e2))
        # then
        assert_that(result, is_(({'id': '1234', 'name': 'Alice'}, {'id': '456'})))

    def test_obj_to_dict_with_object_in_dict(self):
        # given
        e1 = Entry('1234', name='Alice')
        e2 = Entry('456')
        # when
        result = objToDict({'a': e1, 'b': e2})
        # then
        assert_that(result, is_({'a': {'id': '1234', 'name': 'Alice'}, 'b': {'id': '456'}}))
