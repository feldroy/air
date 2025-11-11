# Contributing to examples/src

Air has a system for ensuring that its code examples:

* Can be run as working Air apps
* Have tests that are run in CI and pass

To add a code example:

1. Create a sample Air app file with the naming pattern:

* `module__example.py` where `example` is a function, or
* `module__ClassName.py` where `ClassName` is a class
* `module__ClassName__method_name.py` where `ClassName` is a class and `method_name` is one of its methods

2. Create a test file with the same name + `__test.py`:

* If the Air app file is `module__example.py`, the test is `module__example__test.py`

3. In that test file, write tests for it, following the patterns of the other modules in there