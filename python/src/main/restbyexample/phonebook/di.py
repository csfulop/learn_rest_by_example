"""
Simple python Dependency Injection.

For example:
Instead of directly refer to MemoryPhonebookDbAdapter a dependant should refer PhonebookDbAdapterImpl.
This way it is easy to switch the in-memory DB implementation to MongoDB or whatever else.
"""

from restbyexample.phonebook.db.memory import MemoryPhonebookDbAdapter

PhonebookDbAdapterImpl = MemoryPhonebookDbAdapter
