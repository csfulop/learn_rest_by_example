from unittest import TestCase

from db.adapter import Entry, PhonebookDbException
from db.memory import MemoryPhonebookDbAdapter


class TestMemory(TestCase):
    def setUp(self):
        self.adapter = MemoryPhonebookDbAdapter();

    def test_add_entry(self):
        # given
        entry = Entry()
        entry.id = 1234
        # when
        self.adapter.add(entry)
        # then
        self.assertEqual(self.adapter.size(), 1)

    def test_add_entry_without_id_should_fail(self):
        # given
        entry = Entry()
        # then
        with self.assertRaises(PhonebookDbException):
            # when
            self.adapter.add(entry)

    def test_add_entry_twice_should_replace(self):
        # given
        entry = Entry()
        entry.id = 1234
        entry.name = "Alice"
        # when
        self.adapter.add(entry)
        entry.name = "Bob"
        self.adapter.add(entry)
        # then
        self.assertEqual(self.adapter.size(), 1)
        # FIXME: assert with get
