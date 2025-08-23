"""Example pytest-benchmark test: measures creation throughput for `air.A` tags.

This is intentionally lightweight and intended as an example. Use pytest-benchmark
to run and save/compare results over time.
"""

import air


def test_create_tags_benchmark(benchmark):
    """Benchmark creating a number of `air.A` tag objects.

    The `benchmark` fixture will run the callable multiple times and report
    statistics. Adjust the `n` value to make the workload heavier or lighter.
    """

    def create(n=5000):
        # Create many tag instances; keep this function small and self-contained
        return [air.A(href="/home", class_="link", id=f"elem{i}") for i in range(n)]

    # Run the benchmark with 5000 objects. pytest-benchmark will time this call.
    benchmark(create, 5000)
