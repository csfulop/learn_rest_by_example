from unittest import TestCase

from hamcrest import equal_to
from hamcrest.core import assert_that
from hamcrest.core.core import is_

from restbyexample.phonebook.db.adapter import Entry


class TestEntry(TestCase):
    def test_init_with_id(self):
        entry = Entry(1)
        assert_that(entry.id, is_(1))

    def test_init_with_extra_attrs(self):
        entry = Entry(2, attrBool=True, attrStr='attr', attrDict={'a': 1, 'b': 2})
        assert_that(entry.id, is_(2))
        assert_that(entry.attrBool, is_(True))
        assert_that(entry.attrStr, is_('attr'))
        assert_that(entry.attrDict, equal_to({'a': 1, 'b': 2}))
