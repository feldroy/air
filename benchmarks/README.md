# Benchmarking guide

This directory contains benchmarks using pytest-benchmark and memory checks.

Prerequisites
- Ensure the `test` dependency group is installed (see `pyproject.toml`) which includes pytest.
- Install `pytest-benchmark` to run the microbenchmarks:

  uv sync --group benchmarks

Running benchmarks

- Run all benchmarks in this directory with pytest and the `benchmark` plugin enabled:

```bash
pytest benchmarks -q
```

- Save benchmark results to a JSON file for later comparison:

```bash
pytest benchmarks --benchmark-save=baseline
```

- Compare the current run to a saved baseline:

```bash
pytest benchmarks --benchmark-compare=baseline
```

Memory checks

- Memory-focused tests (tracemalloc) should be marked with a custom marker, e.g. `@pytest.mark.memory`, and run separately since they can be fragile.
- Example: run memory tests only:

```bash
pytest -m memory
```

CI recommendations

- Run microbenchmarks nightly and upload results (JSON) to detect regressions.
- Run memory-retention tests on a scheduled job or release build and keep thresholds flexible to account for interpreter noise.
