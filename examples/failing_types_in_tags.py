"""
These render but demonstrates behavior that should be unacceptable
and will be caught by type checkers. The types help guide LLMs and
type savvy humans. Yet you can pass whatever you want and the code will
still run, which is useful from a development perspective.

To have the failures show up in type checking, remove the # ty: ignore
statements on lines 26, 28, 29, and 30.

Run:
    `just run-py-module examples.failing_types_in_tags`
"""

import air

app = air.Air()


def TestComponent() -> air.BaseTag:
    return air.P("I am a component")


def main() -> None:
    return air.layouts.Body(
        air.Div(
            air.P({}),  # ty: ignore[invalid-argument-type]
            air.P(TestComponent()),
            air.P(TestComponent),  # ty: ignore[invalid-argument-type]
            air.P(air.Span),  # ty: ignore[invalid-argument-type]
            air.P(b"Renders but breaks on types."),  # ty: ignore[invalid-argument-type]
        )
    ).pretty_print()


if __name__ == "__main__":
    main()
