from unittest import TestCase

from hamcrest import not_none, instance_of, equal_to, raises, calling
from hamcrest.core import assert_that
from hamcrest.core.core import is_

from restbyexample.phonebook.db.adapter import Entry, PhonebookDbException
from restbyexample.phonebook.db.memory import MemoryPhonebookDbAdapter


class TestMemory(TestCase):
    def setUp(self):
        self.adapter = MemoryPhonebookDbAdapter()

    def test_add_entry(self):
        # given
        entry = Entry('1234')
        # when
        self.adapter.add(entry)
        # then
        assert_that(self.adapter.size(), is_(1))

    def test_add_entry_without_id_should_generate_random_id(self):
        # given
        entry = Entry(name='Alice')
        # when
        self.adapter.add(entry)
        # then
        assert_that(entry.id, not_none())
        assert_that(entry.id, instance_of(str))

    def test_add_same_id_twice_should_fail(self):
        # given
        id = '1234'
        entry1 = Entry(id, name='Alice')
        entry2 = Entry(id, name='Bob')
        self.adapter.add(entry1)
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.add(entry2)
        assert_that(self.adapter.size(), is_(1))
        assert_that(self.adapter.get(id), equal_to(entry1))

    def test_add_should_deepcopy_the_entry(self):
        # given
        entry = Entry('1234', name='Alice')
        # when
        self.adapter.add(entry)
        # then
        entry.name = 'Bob'
        assert_that(self.adapter.get(entry.id).name, is_('Alice'))

    def test_get_entry(self):
        # given
        entry = Entry('1234', name='Alice')
        self.adapter.add(entry)
        # when
        result = self.adapter.get(entry.id)
        # then
        assert_that(result, equal_to(entry))

    def test_get_should_return_none_if_no_entry_found(self):
        # when
        result = self.adapter.get(123)
        # then
        self.assertIsNone(result)

    def test_get_should_deepcopy_the_entry(self):
        # given
        entry = Entry('1234', name='Alice')
        self.adapter.add(entry)
        # when
        result = self.adapter.get(entry.id)
        # then
        result.name = 'Bob'
        assert_that(self.adapter.get(entry.id).name, is_('Alice'))

    def test_remove(self):
        # given
        entry = Entry(name='Alice')
        self.adapter.add(entry)
        assert_that(self.adapter.size(), is_(1))
        # when
        self.adapter.remove(entry.id)
        # then
        assert_that(self.adapter.size(), is_(0))

    def test_remove_should_fail_if_no_entry(self):
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.remove(1)

    def test_modify(self):
        # given
        entry1 = Entry(name='Alice', id='1234')
        self.adapter.add(entry1)
        entry2 = Entry(name='Bob', id='1234')
        # when
        self.adapter.modify(entry2)
        # then
        assert_that(self.adapter.get('1234'), equal_to(entry2))

    def test_modify_should_fail_without_id(self):
        # given
        entry = Entry(name='Alice')
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.modify(entry)

    def test_modify_not_existing_entry_should_fail(self):
        # given
        entry = Entry(name='Alice', id='1234')
        assert_that(
            # when
            calling(self.adapter.modify).with_args(entry),
            # then
            raises(PhonebookDbException))

    def test_modify_should_deepcopy_the_entry(self):
        # given
        entry = Entry('1234', name='Alice')
        self.adapter.add(entry)
        entry.name = 'Bob'
        # when
        self.adapter.modify(entry)
        # then
        entry.name = 'Charlie'
        assert_that(self.adapter.get(entry.id).name, is_('Bob'))

    def test_list(self):
        assert_that(len(self.adapter.list()), is_(0))
        self.adapter.add(Entry(name='Alice'))
        assert_that(len(self.adapter.list()), is_(1))
        self.adapter.add(Entry(name='Bob'))
        assert_that(len(self.adapter.list()), is_(2))

    def test_list_should_deepcopy_the_entries(self):
        # given
        entry = Entry('1234', name='Alice')
        self.adapter.add(entry)
        # when
        result = self.adapter.list()[0]
        # then
        result.name = 'Bob'
        assert_that(self.adapter.get(entry.id).name, is_('Alice'))
