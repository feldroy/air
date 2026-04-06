"""Whole-app coherence checks for Air applications.

These checks catch problems that linters and type checkers cannot:
route conflicts, missing templates, path parameter mismatches.
"""

from __future__ import annotations

import ast
import inspect
import re
import textwrap
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

import jinja2
from fastapi.routing import APIRoute

if TYPE_CHECKING:
    from .applications import Air


@dataclass
class CheckMessage:
    """A single problem found by a check."""

    category: str
    level: Literal["error", "warning"]
    subject: str
    message: str


@dataclass
class CheckResult:
    """Aggregated output from all checks."""

    messages: list[CheckMessage] = field(default_factory=list)
    route_count: int = 0

    @property
    def errors(self) -> list[CheckMessage]:
        return [m for m in self.messages if m.level == "error"]

    @property
    def warnings(self) -> list[CheckMessage]:
        return [m for m in self.messages if m.level == "warning"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def check_duplicate_routes(app: Air) -> list[CheckMessage]:
    """Flag routes where the same path and method are registered twice."""
    seen: dict[tuple[str, str], list[str]] = {}
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        for method in route.methods or set():
            if method == "HEAD":
                continue
            key = (route.path, method)
            name = route.name or "unknown"
            seen.setdefault(key, []).append(name)

    messages: list[CheckMessage] = []
    for (path, method), names in seen.items():
        if len(names) > 1:
            messages.append(
                CheckMessage(
                    category="routes",
                    level="error",
                    subject=f"{method}  {path}",
                    message=f"duplicate ({', '.join(names)})",
                )
            )
    return messages


def check_path_params(app: Air) -> list[CheckMessage]:
    """Flag route path parameters that don't match the handler signature."""
    messages: list[CheckMessage] = []
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        path_params = set(re.findall(r"\{(\w+)(?::[^}]+)?\}", route.path))
        if not path_params:
            continue

        try:
            original = inspect.unwrap(route.endpoint)
            sig = inspect.signature(original)
        except (TypeError, ValueError):
            continue

        handler_params = set(sig.parameters.keys())
        missing = path_params - handler_params
        if missing:
            method = next(iter((route.methods or set()) - {"HEAD"}), "???")
            messages.append(
                CheckMessage(
                    category="routes",
                    level="error",
                    subject=f"{method}  {route.path}",
                    message=f"path has {{{', '.join(sorted(missing))}}}, handler is missing them",
                )
            )
    return messages


def _extract_template_names(func: object) -> list[str]:
    """Best-effort extraction of template names from a handler's source.

    Looks for calls like ``app.jinja(request, 'name.html')`` or
    ``self.jinja(request, 'name.html')`` and returns the string literal names.
    Dynamic names (f-strings, variables) are not detected.
    """
    try:
        source = inspect.getsource(inspect.unwrap(func))  # type: ignore[arg-type]
    except (TypeError, OSError):
        return []

    # Dedent so ast.parse works on methods/nested functions
    source = textwrap.dedent(source)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    names: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        # Match *.jinja(..., 'name.html', ...)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "jinja" and len(node.args) >= 2:
            arg = node.args[1]
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                names.append(arg.value)
    return names


def check_template_references(app: Air) -> list[CheckMessage]:
    """Flag template names referenced in handlers that don't exist on disk."""
    messages: list[CheckMessage] = []
    env = app.jinja.templates.env
    if env.loader is None:
        return messages

    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        template_names = _extract_template_names(route.endpoint)
        for tpl_name in template_names:
            try:
                env.loader.get_source(env, tpl_name)
            except jinja2.TemplateNotFound:
                handler_name = getattr(inspect.unwrap(route.endpoint), "__name__", "unknown")
                messages.append(
                    CheckMessage(
                        category="templates",
                        level="error",
                        subject=tpl_name,
                        message=f"referenced by {handler_name}() but not found",
                    )
                )
    return messages


def check_template_syntax(app: Air) -> list[CheckMessage]:
    """Pre-compile all templates and flag syntax errors."""
    messages: list[CheckMessage] = []
    env = app.jinja.templates.env
    if env.loader is None:
        return messages

    try:
        template_names = env.loader.list_templates()
    except TypeError:
        return messages

    for name in template_names:
        try:
            source = env.loader.get_source(env, name)[0]
            env.parse(source)
        except jinja2.TemplateSyntaxError as e:
            lineno = f":{e.lineno}" if e.lineno else ""
            messages.append(
                CheckMessage(
                    category="templates",
                    level="error",
                    subject=f"{name}{lineno}",
                    message=str(e.message) if e.message else "syntax error",
                )
            )
    return messages


def run_checks(app: Air) -> CheckResult:
    """Run all checks and return the aggregated result."""
    route_count = sum(1 for r in app.routes if isinstance(r, APIRoute))

    messages: list[CheckMessage] = []
    messages.extend(check_duplicate_routes(app))
    messages.extend(check_path_params(app))
    messages.extend(check_template_references(app))
    messages.extend(check_template_syntax(app))

    return CheckResult(messages=messages, route_count=route_count)
