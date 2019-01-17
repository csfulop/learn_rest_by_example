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

    # FIXME: add should deep copy the entry

    def test_add_entry_without_id_should_generatge_random_id(self):
        # given
        entry = Entry()
        entry.name = "Alice"
        # when
        self.adapter.add(entry)
        # then
        self.assertIsNotNone(entry.id)

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

    def test_get_entry(self):
        # given
        entry = Entry()
        entry.id = id
        entry.name = "Alice"
        self.adapter.add(entry)
        # when
        result = self.adapter.get(entry.id)
        # then
        self.assertEqual(result, entry)

    # FIXME: get nonexistent entry
