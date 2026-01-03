# Documentation source examples

The `examples/src/` directory contains the runnable source snippets that power Air's documentation.
Each file is a minimal Air application or helper that demonstrates a specific API, and the matching
`__test.py` modules verify that the snippet stays up-to-date.

If you add a new example, mirror the existing naming convention (`module__Example.py`) and include
an accompanying test file. After updating the samples, run the `scripts/copy_src_example_to_callable.py`
helper to synchronize the code into the relevant docstrings.
