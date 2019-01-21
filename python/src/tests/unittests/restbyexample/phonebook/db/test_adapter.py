from unittest import TestCase

from restbyexample.phonebook.db.adapter import Entry


class TestEntry(TestCase):
    def test_init_with_id(self):
        entry = Entry(1)
        self.assertEqual(entry.id, 1)

    def test_init_with_extra_attrs(self):
        entry = Entry(2, attrBool=True, attrStr='attr', attrDict={'a': 1, 'b': 2})
        self.assertEqual(entry.id, 2)
        self.assertEqual(entry.attrBool, True)
        self.assertEqual(entry.attrStr, 'attr')
        self.assertEqual(entry.attrDict, {'a': 1, 'b': 2})
