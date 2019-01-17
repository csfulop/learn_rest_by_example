from unittest import TestCase

from db.adapter import Entry, PhonebookDbException
from db.memory import MemoryPhonebookDbAdapter


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

    def test_get_entry(self):
        # given
        entry = Entry(1234, name='Alice')
        self.adapter.add(entry)
        # when
        result = self.adapter.get(entry.id)
        # then
        self.assertEqual(result, entry)

    def test_add_should_deep_copy_the_entry(self):
        # given
        entry = Entry(1234, name='Alice')
        # when
        self.adapter.add(entry)
        # then
        entry.name = 'Bob'
        self.assertEqual(self.adapter.get(entry.id).name, 'Alice')

    def test_get_should_return_none_if_no_entry_found(self):
        # when
        result = self.adapter.get(123)
        # then
        self.assertIsNone(result)
