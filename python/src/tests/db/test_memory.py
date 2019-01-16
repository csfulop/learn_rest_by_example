from unittest import TestCase

from db.adapter import Entry, PhonebookDbException
from db.memory import MemoryPhonebookDbAdapter


class TestMemory(TestCase):
    def setUp(self):
        self.adapter = MemoryPhonebookDbAdapter()

    def test_add_entry(self):
        # given
        entry = Entry()
        entry.id = 1234
        # when
        self.adapter.add(entry)
        # then
        self.assertEqual(self.adapter.size(), 1)

    def test_add_entry_without_id_should_fail(self):
        # FIXME: should generate random id
        # given
        entry = Entry()
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.add(entry)

    def test_add_same_id_twice_should_fail(self):
        # given
        id = 1234
        entry1 = Entry()
        entry1.id = id
        entry1.name = "Alice"
        entry2 = Entry()
        entry2.id = id
        entry2.name = "Bob"
        self.adapter.add(entry1)
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.add(entry2)
        self.assertEqual(self.adapter.size(), 1)
        self.assertEqual(self.adapter.get(id), entry1)

    # FIXME: test get
