# Benchmarking guide

This directory contains benchmarks using pytest-benchmark and memory checks.

Running benchmarks

- Run all benchmarks with pytest and the `benchmark` plugin enabled:

```bash
uv run -q -- pytest tests/benchmarks -q
```

- Save benchmark results to a JSON file for later comparison:

```bash
uv run -q -- pytest tests/benchmarks --benchmark-save=baseline
```

- Compare the current run to a saved baseline:

```bash
uv run -q -- pytest tests/benchmarks --benchmark-compare=baseline
```

Memory checks

- Memory-focused tests (tracemalloc) should be marked with a custom marker, e.g. `@pytest.mark.memory`, and run separately since they can be fragile.
- Example: run memory tests only:

```bash
uv run -q -- pytest tests/benchmarks -m memory
```
- Print results for memory scaling (bytes per tag)

```bash
uv run -- pytest -s tests/benchmarks -m memory --log-cli-level=INFO
```

CI recommendations

- Run microbenchmarks nightly and upload results (JSON) to detect regressions.
- Run memory-retention tests on a scheduled job or release build and keep thresholds flexible to account for interpreter noise.
