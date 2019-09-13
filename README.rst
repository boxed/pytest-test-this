===============================
pytest-test-this
===============================

Plugin for ``pytest`` to run relevant tests by naively check if test functions contain a reference to the symbol supplied.


Limitations:
    - it only looks for top level test functions, so test classes won't be discovered
    - it only checks files called `test_something`
    - very naive check, so indirect usages of a symbol won't be found

This trade off has been made for speed. This method is extremely fast compared to the other common method which tries to be correct by running the full test suite under coverage and checking if the function was called directly or indirectly.

Installation
------------

    pip install pytest-test-this

Usage
-----

    pytest --test-this=foo

...where foo is the name of your function, class or variable.