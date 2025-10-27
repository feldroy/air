"""Memory tests for Air Tags object cleanup and retention.

These tests use tracemalloc to verify that tag objects are properly
garbage collected and don't leak memory during typical usage patterns.
"""

import gc
import tracemalloc

import pytest

import air
from air import Div, Span


@pytest.mark.memory
def test_tag_object_memory_cleanup() -> None:
    """Verify that creating and destroying many tag objects doesn't leak memory.

    This test ensures that Air Tags are properly garbage collected and don't
    accumulate memory over multiple creation/destruction cycles.
    """

    tracemalloc.start()

    # Get baseline memory usage
    gc.collect()  # Clean up any existing objects
    baseline_snapshot = tracemalloc.take_snapshot()
    baseline_memory = sum(stat.size for stat in baseline_snapshot.statistics("filename"))

    # Create and destroy tags multiple times
    for _cycle in range(10):
        # Create a large number of complex tag structures
        tags = []
        for i in range(1000):
            tag = air.Div(
                air.H2(f"Item {i}", class_="title"),
                air.P(f"Description for item {i}", class_="desc"),
                air.Ul(air.Li(f"Feature {j}", class_="feature") for j in range(5)),
                air.Form(
                    air.Input(type="text", name=f"input_{i}", value=f"value_{i}"),
                    air.Button("Submit", type="submit"),
                    action=f"/submit/{i}",
                    method="post",
                ),
                class_="item-card",
                id=f"item-{i}",
            )
            tags.append(tag)

        # Render all tags to ensure full object initialization
        rendered = [tag.render() for tag in tags]

        # Explicitly delete references
        del tags
        del rendered

        # Force garbage collection
        gc.collect()

    # Measure final memory usage
    final_snapshot = tracemalloc.take_snapshot()
    final_memory = sum(stat.size for stat in final_snapshot.statistics("filename"))

    tracemalloc.stop()

    # Calculate memory growth
    memory_growth = final_memory - baseline_memory

    # Allow for some memory growth but flag significant leaks
    # 1MB tolerance for interpreter overhead and caching
    max_allowed_growth = 1024 * 1024  # 1MB

    assert memory_growth < max_allowed_growth, (
        f"Memory leak detected: {memory_growth:,} bytes growth exceeds threshold of {max_allowed_growth:,} bytes"
    )


@pytest.mark.memory
def test_nested_tag_memory_efficiency() -> None:
    """Test memory usage patterns for deeply nested tag structures.

    Verifies that complex nested structures don't use excessive memory
    and are properly cleaned up.
    """

    tracemalloc.start()

    # Create deeply nested structure
    def create_nested_structure(depth: int = 10) -> Div | Span:
        if depth == 0:
            return air.Span("Deep content", class_="leaf")

        return air.Div(
            air.H3(f"Level {depth}"),
            create_nested_structure(depth - 1),
            air.P(f"Content at level {depth}"),
            class_=f"level-{depth}",
        )

    # Measure memory before creation
    gc.collect()
    start_snapshot = tracemalloc.take_snapshot()
    start_memory = sum(stat.size for stat in start_snapshot.statistics("filename"))

    # Create multiple nested structures
    structures = [create_nested_structure() for _ in range(100)]

    # Render to ensure full initialization
    rendered = [struct.render() for struct in structures]

    # Measure peak memory
    peak_snapshot = tracemalloc.take_snapshot()
    peak_memory = sum(stat.size for stat in peak_snapshot.statistics("filename"))

    # Clean up
    del structures
    del rendered
    gc.collect()

    # Measure final memory
    end_snapshot = tracemalloc.take_snapshot()
    end_memory = sum(stat.size for stat in end_snapshot.statistics("filename"))

    tracemalloc.stop()

    memory_during_use = peak_memory - start_memory
    memory_after_cleanup = end_memory - start_memory
    cleanup_efficiency = 1 - (memory_after_cleanup / memory_during_use) if memory_during_use > 0 else 1

    # Expect at least 80% memory cleanup efficiency
    assert cleanup_efficiency > 0.8, f"Poor memory cleanup: only {cleanup_efficiency:.2%} of memory was freed"

    # Ensure final memory growth is minimal (allow 500KB for interpreter overhead)
    assert memory_after_cleanup < 512 * 1024, f"Excessive memory retention: {memory_after_cleanup:,} bytes remaining"


@pytest.mark.memory
def test_tag_creation_memory_scaling() -> None:
    """Test that tag creation memory usage scales linearly with object count.

    Ensures that Air Tags don't have hidden memory overhead that grows
    non-linearly with the number of objects created.
    """

    tracemalloc.start()

    memory_measurements = []

    # Test different scales of tag creation
    for scale in [100, 500, 1000, 2000]:
        gc.collect()
        before_snapshot = tracemalloc.take_snapshot()
        before_memory = sum(stat.size for stat in before_snapshot.statistics("filename"))

        # Create tags at this scale
        tags = [
            air.Article(
                air.H2(f"Article {i}"),
                air.P(f"Content for article {i}"),
                air.Footer(f"Footer {i}"),
                class_="article",
                id=f"article-{i}",
            )
            for i in range(scale)
        ]

        after_snapshot = tracemalloc.take_snapshot()
        after_memory = sum(stat.size for stat in after_snapshot.statistics("filename"))

        memory_used = after_memory - before_memory
        memory_per_tag = memory_used / scale

        memory_measurements.append((scale, memory_used, memory_per_tag))

        # Clean up for next iteration
        del tags
        gc.collect()

    tracemalloc.stop()

    # TODO:
    #   Print memory scaling results
    #   for scale, _total_memory, _per_tag_memory in memory_measurements:
    #       pass

    # Check that memory per tag is relatively consistent (within 50% variance)
    per_tag_memories = [measurement[2] for measurement in memory_measurements]
    min_per_tag = min(per_tag_memories)
    max_per_tag = max(per_tag_memories)
    variance_ratio = max_per_tag / min_per_tag

    assert variance_ratio < 1.5, f"Memory scaling is non-linear: {variance_ratio:.2f}x variance in per-tag memory usage"

    # Ensure reasonable memory usage per tag (complex tags with nested elements)
    # These are Article tags with H2, P, and Footer children, so ~1.2KB is reasonable
    avg_per_tag = sum(per_tag_memories) / len(per_tag_memories)
    assert avg_per_tag < 2048, f"Excessive memory per tag: {avg_per_tag:.1f} bytes/tag exceeds 2KB threshold"
