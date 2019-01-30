REST API with Pecan
===================

Quick start example
-------------------

https://pecan.readthedocs.io/en/latest/quick_start.html

To create a skeleton with the example:
`pecan create test_project`

Update `config.py` with the root controller, module names and paths.

To execute the example:
`pecan serve config.py`

REST example
------------

https://pecan.readthedocs.io/en/latest/rest.html

Phonebook example
-----------------

Implementing REST API with Generic Controllers is quite cumbersome.

For example: In case the URL finishes with an ID
then you either end the URL with a trailing slash
(`http://localhost:800/phonebook/1234/`)
or without trailing slap Pecan will send 302 redirect to an URL with the trailing slash.    
With Generic Controller you have to hack the routing of Pecan to make it work
without the trailing slash.

It is easier to extend RestController of Pecan.