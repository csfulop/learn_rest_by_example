from unittest import TestCase

from db.memory import MemoryPhonebookAdapter


class TestMemory(TestCase):
    def test_create_adapter(self):
        adapter = MemoryPhonebookAdapter();
