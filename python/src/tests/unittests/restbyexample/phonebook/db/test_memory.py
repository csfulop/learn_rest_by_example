from unittest import TestCase

from restbyexample.phonebook.db.adapter import Entry, PhonebookDbException
from restbyexample.phonebook.db.memory import MemoryPhonebookDbAdapter


class TestMemory(TestCase):
    def setUp(self):
        self.adapter = MemoryPhonebookDbAdapter()

    def test_add_entry(self):
        # given
        entry = Entry(1234)
        # when
        self.adapter.add(entry)
        # then
        self.assertEqual(self.adapter.size(), 1)

    def test_add_entry_without_id_should_generatge_random_id(self):
        # given
        entry = Entry(name='Alice')
        # when
        self.adapter.add(entry)
        # then
        self.assertIsNotNone(entry.id)

    def test_add_same_id_twice_should_fail(self):
        # given
        id = 1234
        entry1 = Entry(id, name='Alice')
        entry2 = Entry(id, name='Bob')
        self.adapter.add(entry1)
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.add(entry2)
        self.assertEqual(self.adapter.size(), 1)
        self.assertEqual(self.adapter.get(id), entry1)

    def test_add_should_deepcopy_the_entry(self):
        # given
        entry = Entry(1234, name='Alice')
        # when
        self.adapter.add(entry)
        # then
        entry.name = 'Bob'
        self.assertEqual(self.adapter.get(entry.id).name, 'Alice')

    def test_get_entry(self):
        # given
        entry = Entry(1234, name='Alice')
        self.adapter.add(entry)
        # when
        result = self.adapter.get(entry.id)
        # then
        self.assertEqual(result, entry)

    def test_get_should_return_none_if_no_entry_found(self):
        # when
        result = self.adapter.get(123)
        # then
        self.assertIsNone(result)

    def test_get_should_deepcopy_the_entry(self):
        # given
        entry = Entry(1234, name='Alice')
        self.adapter.add(entry)
        # when
        result = self.adapter.get(entry.id)
        # then
        result.name = 'Bob'
        self.assertEqual(self.adapter.get(entry.id).name, 'Alice')

    def test_remove(self):
        # given
        entry = Entry(name='Alice')
        self.adapter.add(entry)
        self.assertEqual(self.adapter.size(), 1)
        # when
        self.adapter.remove(entry.id)
        # then
        self.assertEqual(self.adapter.size(), 0)

    def test_remove_should_fail_if_no_entry(self):
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.remove(1)

    def test_list(self):
        self.assertEqual(len(self.adapter.list()), 0)
        self.adapter.add(Entry(name='Alice'))
        self.assertEqual(len(self.adapter.list()), 1)
        self.adapter.add(Entry(name='Bob'))
        self.assertEqual(len(self.adapter.list()), 2)

    def test_list_should_deepcopy_the_entries(self):
        # given
        entry = Entry(1234, name='Alice')
        self.adapter.add(entry)
        # when
        result = self.adapter.list()[0]
        # then
        result.name = 'Bob'
        self.assertEqual(self.adapter.get(entry.id).name, 'Alice')
