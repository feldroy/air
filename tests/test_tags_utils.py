from __future__ import annotations

import builtins
import sys
import types
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import pytest

import air.tags.utils as utils
from air.exceptions import BrowserOpenError
from air.tags.utils import SafeStr


@pytest.fixture
def stub_lxml(monkeypatch: pytest.MonkeyPatch) -> Iterator[dict[str, Any]]:
    captured: dict[str, Any] = {}

    class DummyNode:
        def __init__(self, label: str) -> None:
            self.label = label
            self.indented = False

    def document_fromstring(source: str, *, ensure_head_body: bool) -> DummyNode:
        node = DummyNode(f"doc::{source}::{ensure_head_body}")
        captured["document"] = node
        return node

    def fromstring(source: str) -> DummyNode:
        node = DummyNode(f"node::{source}")
        captured["node"] = node
        return node

    def indent(node: DummyNode) -> None:
        node.indented = True

    def tostring(node: DummyNode, encoding: str, *, pretty_print: bool, doctype: str | None) -> str:
        captured["serialized"] = (node.label, encoding, pretty_print, doctype)
        return f"serialized::{node.label}::{encoding}::{pretty_print}::{doctype}"

    lxml_module = types.ModuleType("lxml")
    etree_module = types.ModuleType("lxml.etree")
    html_module = types.ModuleType("lxml.html")

    etree_module.indent = indent
    html_module.document_fromstring = document_fromstring
    html_module.fromstring = fromstring
    html_module.tostring = tostring

    lxml_module.etree = etree_module
    lxml_module.html = html_module

    monkeypatch.setitem(sys.modules, "lxml", lxml_module)
    monkeypatch.setitem(sys.modules, "lxml.etree", etree_module)
    monkeypatch.setitem(sys.modules, "lxml.html", html_module)

    yield captured

    monkeypatch.delitem(sys.modules, "lxml", raising=False)
    monkeypatch.delitem(sys.modules, "lxml.etree", raising=False)
    monkeypatch.delitem(sys.modules, "lxml.html", raising=False)


@pytest.fixture
def stub_rich(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    printed: list[dict[str, Any]] = []

    class ConsoleStub:
        def __init__(self, *, record: bool, file: Any) -> None:
            self.record = record
            self.file = file
            self.printed: list[dict[str, Any]] = []
            self.saved_path: str | None = None

        def print(self, panel: Any, *, soft_wrap: bool) -> None:
            self.printed.append({"panel": panel, "soft_wrap": soft_wrap})
            printed.append({"panel": panel, "soft_wrap": soft_wrap})

        def save_html(self, path: str) -> None:
            self.saved_path = path

        def export_html(self) -> str:
            return "exported html"

    @dataclass(slots=True)
    class SyntaxStub:
        source: str
        lexer: str
        theme: str
        line_numbers: bool
        indent_guides: bool
        word_wrap: bool

    @dataclass(slots=True)
    class TextStub:
        text: str
        style: str

    class PanelStub:
        @classmethod
        def fit(
            cls,
            renderable: Any,
            *,
            box: Any,
            border_style: str,
            title: TextStub,
        ) -> dict[str, Any]:
            return {
                "renderable": renderable,
                "box": box,
                "border_style": border_style,
                "title": title,
            }

    box_module = types.ModuleType("rich.box")
    box_module.HEAVY = "HEAVY"

    console_module = types.ModuleType("rich.console")
    console_module.Console = ConsoleStub

    panel_module = types.ModuleType("rich.panel")
    panel_module.Panel = PanelStub

    syntax_module = types.ModuleType("rich.syntax")
    syntax_module.Syntax = SyntaxStub

    text_module = types.ModuleType("rich.text")
    text_module.Text = TextStub

    rich_module = types.ModuleType("rich")
    rich_module.box = box_module
    rich_module.console = console_module
    rich_module.panel = panel_module
    rich_module.syntax = syntax_module
    rich_module.text = text_module

    monkeypatch.setitem(sys.modules, "rich", rich_module)
    monkeypatch.setitem(sys.modules, "rich.box", box_module)
    monkeypatch.setitem(sys.modules, "rich.console", console_module)
    monkeypatch.setitem(sys.modules, "rich.panel", panel_module)
    monkeypatch.setitem(sys.modules, "rich.syntax", syntax_module)
    monkeypatch.setitem(sys.modules, "rich.text", text_module)

    return {"Console": ConsoleStub, "printed": printed}


def test_clean_html_attr_key_transforms_special_suffixes() -> None:
    assert utils.clean_html_attr_key("class_") == "class"
    assert utils.clean_html_attr_key("__data_value") == "data-value"


def test_pretty_format_html_unescapes_entities(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_format_html(source: str, **kwargs: bool) -> str:
        assert kwargs["pretty"] is True
        return "&lt;div&gt;text&lt;/div&gt;"

    monkeypatch.setattr(utils, "format_html", fake_format_html)

    result = utils.pretty_format_html("<div/>", with_body=True, with_doctype=True)

    assert result == "<div>text</div>"


def test_format_html_uses_lxml_document_path(stub_lxml: dict[str, Any]) -> None:
    result = utils.format_html("<p/>", with_body=True, with_head=True, with_doctype=True, pretty=True)

    assert result == "serialized::doc::<p/>::True::unicode::True::<!doctype html>"
    assert stub_lxml["document"].indented is True


def test_format_html_uses_lxml_fragment_path(stub_lxml: dict[str, Any]) -> None:
    result = utils.format_html("<span/>", with_body=False, pretty=False)

    assert result == "serialized::node::<span/>::unicode::False::None"
    assert stub_lxml["node"].indented is False


def test_format_html_requires_lxml(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def fake_import(
        name: str,
        globals_: dict[str, Any] | None = None,
        locals_: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name.startswith("lxml"):
            raise ModuleNotFoundError
        return original_import(name, globals_, locals_, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(ModuleNotFoundError) as exc:
        utils.format_html("<p/>")

    assert "Extra feature 'pretty'" in str(exc.value)


def test_open_local_file_in_the_browser_accepts_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    file_path = tmp_path / "sample.html"
    file_path.write_text("<html></html>")
    opened: list[str] = []

    def record(url: str) -> None:
        opened.append(url)

    monkeypatch.setattr(utils, "_open_new_tab", record)

    utils.open_local_file_in_the_browser(file_path)

    assert opened[0].startswith("file://")


def test_open_local_file_in_the_browser_accepts_directories(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    directory = tmp_path / "site"
    directory.mkdir()
    (directory / "index.html").write_text("<html></html>")
    opened: list[str] = []

    def record(url: str) -> None:
        opened.append(url)

    monkeypatch.setattr(utils, "_open_new_tab", record)

    utils.open_local_file_in_the_browser(directory)

    assert opened[0].endswith("index.html")


def test_open_local_file_in_the_browser_requires_existing_path(tmp_path: Path) -> None:
    target = tmp_path / "missing.html"

    with pytest.raises(FileNotFoundError):
        utils.open_local_file_in_the_browser(target)


def test_open_new_tab_success(monkeypatch: pytest.MonkeyPatch) -> None:
    visited: list[str] = []

    def record(url: str) -> bool:
        visited.append(url)
        return True

    monkeypatch.setattr(utils.webbrowser, "open_new_tab", record)

    utils._open_new_tab("https://example.com")

    assert visited == ["https://example.com"]


def test_open_new_tab_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def deny(url: str) -> bool:
        return False

    monkeypatch.setattr(utils.webbrowser, "open_new_tab", deny)

    with pytest.raises(BrowserOpenError):
        utils._open_new_tab("https://example.com")


def test_open_html_blob_in_the_browser_uses_data_url(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[str] = []

    def record(url: str) -> None:
        opened.append(url)

    monkeypatch.setattr(utils, "_open_new_tab", record)

    utils.open_html_blob_in_the_browser("<p>hi</p>")

    assert opened[0].startswith(utils.BLOB_URL_PRESET)


def test_open_html_blob_in_the_browser_limits_size(monkeypatch: pytest.MonkeyPatch) -> None:
    def noop(url: str) -> None:
        return None

    monkeypatch.setattr(utils, "_open_new_tab", noop)

    with pytest.raises(utils.URLError):
        utils.open_html_blob_in_the_browser("x", data_url_max=len(utils.BLOB_URL_PRESET) + 1)


def test_open_html_in_the_browser_writes_temp_file(monkeypatch: pytest.MonkeyPatch) -> None:
    opened: list[str] = []

    def record(url: str) -> None:
        opened.append(url)

    monkeypatch.setattr(utils, "_open_new_tab", record)

    utils.open_html_in_the_browser("<article></article>")

    assert opened and opened[0].startswith("file://")


def test_save_pretty_html_uses_console(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    saved: list[str] = []

    @dataclass(slots=True)
    class RecordingConsole:
        record: bool
        file: Any

        def save_html(self, path: str) -> None:
            saved.append(path)

    def fake_get_pretty_html_console(source: str, theme: str, *, record: bool) -> RecordingConsole:
        return RecordingConsole(record=record, file=None)

    monkeypatch.setattr(utils, "_get_pretty_html_console", fake_get_pretty_html_console)

    utils.save_pretty_html("<html/>", theme="default", file_path=tmp_path / "pretty.html")

    assert saved == [str(tmp_path / "pretty.html")]


def test_display_pretty_html_in_the_browser_uses_export(monkeypatch: pytest.MonkeyPatch) -> None:
    exported: list[str] = []
    displayed: list[str] = []

    def fake_export(source: str, theme: str) -> str:
        exported.append(source)
        return "exported"

    def fake_open(html: str) -> None:
        displayed.append(html)

    monkeypatch.setattr(utils, "export_pretty_html", fake_export)
    monkeypatch.setattr(utils, "open_html_in_the_browser", fake_open)

    utils.display_pretty_html_in_the_browser("<body></body>", theme="dracula")

    assert exported == ["<body></body>"]
    assert displayed == ["exported"]


def test_export_pretty_html_uses_console(monkeypatch: pytest.MonkeyPatch) -> None:
    class RecordingConsole:
        def __init__(self, *, record: bool, file: Any) -> None:
            self.record = record
            self.file = file

        def export_html(self) -> str:
            return "panel"

    def fake_get_pretty_html_console(source: str, theme: str, *, record: bool) -> RecordingConsole:
        return RecordingConsole(record=record, file=None)

    monkeypatch.setattr(utils, "_get_pretty_html_console", fake_get_pretty_html_console)

    result = utils.export_pretty_html("<html/>", theme="solarized")

    assert result == "panel"


def test_pretty_print_html_delegates_to_console(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[dict[str, Any]] = []

    @dataclass(slots=True)
    class RecordingConsole:
        record: bool
        file: Any

    def fake_get_pretty_html_console(source: str, theme: str, *, record: bool) -> RecordingConsole:
        captured.append({"source": source, "theme": theme, "record": record})
        return RecordingConsole(record=record, file=None)

    monkeypatch.setattr(utils, "_get_pretty_html_console", fake_get_pretty_html_console)

    utils.pretty_print_html("<html/>", theme="default", record=True)

    assert captured == [{"source": "<html/>", "theme": "default", "record": True}]


def test_get_pretty_html_console_builds_panel(stub_rich: dict[str, Any]) -> None:
    console = utils._get_pretty_html_console("<p/>", theme="monokai", record=True)

    assert isinstance(console, stub_rich["Console"])
    assert console.record is True
    printed = cast(list[dict[str, Any]], stub_rich["printed"])
    assert printed
    panel_info = printed[0]
    assert panel_info["soft_wrap"] is False


def test_get_pretty_html_console_requires_rich(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__

    def fake_import(
        name: str,
        globals_: dict[str, Any] | None = None,
        locals_: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name.startswith("rich"):
            raise ModuleNotFoundError
        return original_import(name, globals_, locals_, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(ModuleNotFoundError):
        utils._get_pretty_html_console("<p/>", theme="monokai", record=False)


def test_locals_cleanup_filters_values() -> None:
    data = {
        "href": "/home",
        "class_": "link",
        "none_value": None,
        "_private": "x",
        "self": "ignored",
    }

    result = utils.locals_cleanup(data)

    assert result == {"href": "/home", "class_": "link"}


def test_locals_cleanup_respects_skip_override() -> None:
    data = {
        "custom": "x",
        "args": "ignored",
    }

    result = utils.locals_cleanup(data, _skip=frozenset({"args"}))

    assert result == {"custom": "x"}


def test_safestr_behaves_like_str() -> None:
    safe = SafeStr("<strong>safe</strong>")

    assert isinstance(safe, str)
    assert str(safe) == "<strong>safe</strong>"
