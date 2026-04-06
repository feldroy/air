"""Tests for air.checks -- whole-app coherence validation."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

import air
from air.checks import (
    CheckResult,
    check_duplicate_routes,
    check_path_params,
    check_template_references,
    check_template_syntax,
    run_checks,
)
from air.cli import app as cli_app
from air.templating import JinjaRenderer

# ── Duplicate routes ─────────────────────────────────────────────────


def test_duplicate_routes_detected() -> None:
    a = air.Air()

    @a.get("/items")
    def list_items() -> air.H1:
        return air.H1("one")

    @a.get("/items")
    def list_items_v2() -> air.H1:
        return air.H1("two")

    msgs = check_duplicate_routes(a)
    assert len(msgs) == 1
    assert msgs[0].level == "error"
    assert "duplicate" in msgs[0].message
    assert "list_items" in msgs[0].message
    assert "list_items_v2" in msgs[0].message


def test_different_methods_same_path_ok() -> None:
    a = air.Air()

    @a.get("/items")
    def get_items() -> air.H1:
        return air.H1("get")

    @a.post("/items")
    def create_item() -> air.H1:
        return air.H1("post")

    msgs = check_duplicate_routes(a)
    assert msgs == []


def test_no_routes_ok() -> None:
    a = air.Air()
    msgs = check_duplicate_routes(a)
    assert msgs == []


# ── Path parameter mismatches ────────────────────────────────────────


def test_path_param_mismatch_detected() -> None:
    a = air.Air()

    @a.get("/users/{user_id}")
    def get_user(user_name: int) -> air.H1:
        return air.H1(f"user {user_name}")

    msgs = check_path_params(a)
    assert len(msgs) == 1
    assert msgs[0].level == "error"
    assert "user_id" in msgs[0].message


def test_path_params_match_ok() -> None:
    a = air.Air()

    @a.get("/users/{user_id}")
    def get_user(user_id: int) -> air.H1:
        return air.H1(f"user {user_id}")

    msgs = check_path_params(a)
    assert msgs == []


def test_no_path_params_ok() -> None:
    a = air.Air()

    @a.get("/health")
    def health() -> air.H1:
        return air.H1("ok")

    msgs = check_path_params(a)
    assert msgs == []


def test_multiple_path_params_partial_mismatch() -> None:
    a = air.Air()

    @a.get("/orgs/{org_id}/repos/{repo_id}")
    def get_repo(org_id: int, wrong_name: int) -> air.H1:
        return air.H1(f"{org_id} {wrong_name}")

    msgs = check_path_params(a)
    assert len(msgs) == 1
    assert "repo_id" in msgs[0].message


def test_typed_path_param_mismatch_detected() -> None:
    a = air.Air()

    @a.get("/users/{user_id:int}")
    def get_user(wrong_name: int) -> air.H1:
        return air.H1(f"user {wrong_name}")

    msgs = check_path_params(a)
    assert len(msgs) == 1
    assert "user_id" in msgs[0].message


def test_typed_path_param_match_ok() -> None:
    a = air.Air()

    @a.get("/items/{item_id:int}")
    def get_item(item_id: int) -> air.H1:
        return air.H1(f"item {item_id}")

    msgs = check_path_params(a)
    assert msgs == []


def test_duplicate_routes_with_router() -> None:
    a = air.Air()
    router = air.AirRouter(prefix="/api")

    @router.get("/items")
    def list_items() -> air.H1:
        return air.H1("one")

    a.include_router(router)

    @a.get("/api/items")
    def list_items_v2() -> air.H1:
        return air.H1("two")

    msgs = check_duplicate_routes(a)
    assert len(msgs) == 1
    assert "duplicate" in msgs[0].message


# ── Template references ──────────────────────────────────────────────


def test_missing_template_reference(tmp_path: object) -> None:
    tpl_dir = Path(str(tmp_path)) / "templates"
    tpl_dir.mkdir()

    a = air.Air()
    a.jinja = JinjaRenderer(str(tpl_dir))

    @a.get("/")
    def index(request: air.Request) -> air.H1:
        return a.jinja(request, "missing.html")  # type: ignore[return-value]

    msgs = check_template_references(a)
    assert len(msgs) == 1
    assert msgs[0].level == "error"
    assert "missing.html" in msgs[0].subject
    assert "index" in msgs[0].message


def test_existing_template_ok(tmp_path: object) -> None:
    tpl_dir = Path(str(tmp_path)) / "templates"
    tpl_dir.mkdir()
    (tpl_dir / "home.html").write_text("<h1>Hello</h1>")

    a = air.Air()
    a.jinja = JinjaRenderer(str(tpl_dir))

    @a.get("/")
    def index(request: air.Request) -> air.H1:
        return a.jinja(request, "home.html")  # type: ignore[return-value]

    msgs = check_template_references(a)
    assert msgs == []


def test_no_jinja_calls_ok() -> None:
    a = air.Air()

    @a.get("/")
    def index() -> air.H1:
        return air.H1("no templates")

    msgs = check_template_references(a)
    assert msgs == []


# ── Template syntax errors ───────────────────────────────────────────


def test_template_syntax_error_detected(tmp_path: object) -> None:
    tpl_dir = Path(str(tmp_path)) / "templates"
    tpl_dir.mkdir()
    (tpl_dir / "bad.html").write_text("{% block title %}unclosed")

    a = air.Air()
    a.jinja = JinjaRenderer(str(tpl_dir))

    msgs = check_template_syntax(a)
    assert len(msgs) == 1
    assert msgs[0].level == "error"
    assert "bad.html" in msgs[0].subject


def test_valid_templates_ok(tmp_path: object) -> None:
    tpl_dir = Path(str(tmp_path)) / "templates"
    tpl_dir.mkdir()
    (tpl_dir / "good.html").write_text("<h1>{{ title }}</h1>")

    a = air.Air()
    a.jinja = JinjaRenderer(str(tpl_dir))

    msgs = check_template_syntax(a)
    assert msgs == []


def test_no_templates_dir_ok() -> None:
    a = air.Air()
    msgs = check_template_syntax(a)
    assert msgs == []


# ── run_checks orchestrator ──────────────────────────────────────────


def test_run_checks_clean_app() -> None:
    a = air.Air()

    @a.get("/hello")
    def hello() -> air.H1:
        return air.H1("hi")

    result = run_checks(a)
    assert isinstance(result, CheckResult)
    assert result.ok
    assert result.route_count >= 1
    assert result.errors == []
    assert result.warnings == []


def test_run_checks_with_errors() -> None:
    a = air.Air()

    @a.get("/items")
    def handler_a() -> air.H1:
        return air.H1("a")

    @a.get("/items")
    def handler_b() -> air.H1:
        return air.H1("b")

    result = run_checks(a)
    assert not result.ok
    assert len(result.errors) >= 1


# ── CLI integration ──────────────────────────────────────────────────


def test_cli_check_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli_app, ["check", "--help"], color=False)
    assert result.exit_code == 0
    assert "Check" in result.output


def test_cli_check_import_failure() -> None:
    runner = CliRunner()
    result = runner.invoke(cli_app, ["check", "nonexistent_module:app"], color=False)
    assert result.exit_code == 1
    assert "Could not import app" in result.output
