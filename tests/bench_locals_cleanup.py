"""Quick benchmark to check for memory leaks when creating many tag instances.

This script constructs many `air.A` tag objects which trigger
`locals_cleanup` via the tag constructors, snapshots memory before and after,
then deletes references to ensure memory is freed.
"""

import gc
import statistics
import tracemalloc

import air


def create_many(n):
    objs = []
    for i in range(n):
        # Keep objects alive initially to measure retained memory
        objs.append(air.A(href="/home", class_="link", id=f"elem{i}"))
    return objs


def snapshot_diff(s1, s2, limit=10):
    stats = s2.compare_to(s1, "lineno")
    for stat in stats[:limit]:
        print(stat)


def main():
    tracemalloc.start()
    gc.collect()

    snap1 = tracemalloc.take_snapshot()
    objs = create_many(5000)
    snap2 = tracemalloc.take_snapshot()

    print("Top allocations after creating objects:")
    snapshot_diff(snap1, snap2, limit=10)

    # Now drop references and force GC
    del objs
    gc.collect()

    snap3 = tracemalloc.take_snapshot()
    print("Top allocations after deleting objects and GC:")
    snapshot_diff(snap2, snap3, limit=10)


if __name__ == "__main__":
    main()
