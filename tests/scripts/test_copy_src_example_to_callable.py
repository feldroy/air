import time

import subprocess


import pytest

from pathlib import Path

from scripts.copy_src_example_to_callable import (
    remove_python_extension,
    split_name_by_double_underscore,
    parse_funtion_module_and_class_from_filename,
    update_example_section,
)


@pytest.mark.solo
@pytest.mark.parametrize(
    "filename, expected_output",
    [
        ("applications.py", "applications"),
        ("requests.py", "requests"),
        ("utils.py", "utils"),
        ("template_tags.py", "template_tags"),
        ("session_management.py", "session_management"),
    ],
)
def test_remove_python_extension_returns_filename_without_py_extension(
    filename: str, expected_output: str
) -> None:
    """remove_python_extension() returns filename without .py extension."""
    assert remove_python_extension(filename) == expected_output


@pytest.mark.solo
@pytest.mark.parametrize(
    "filename",
    [
        "getCallable.js",
        "example.txt",
        "data.json",
        "script.sh",
        "README.md",
    ],
)
def test_remove_python_extension_raises_ValueError_on_non_python_files(
    filename: str,
) -> None:
    """remove_python_extension() raises ValueError when filename is not a python file name."""
    with pytest.raises(ValueError):
        remove_python_extension(filename)


@pytest.mark.solo
@pytest.mark.parametrize(
    "filename, expected_output",
    [
        ("applications__Air__get", ["applications", "Air", "get"]),
        ("applications__Air__page", ["applications", "Air", "page"]),
        ("applications__Air__post", ["applications", "Air", "post"]),
    ],
)
def test_split_name_by_double_underscore_returns_expected_output(
    filename: str, expected_output: list[str]
) -> None:
    """split_name_by_double_underscore() returns expected list of strings from double underscore split."""
    assert split_name_by_double_underscore(filename) == expected_output


@pytest.mark.solo
def test_parse_funtion_module_and_class_from_filename_returns_None_on_filename_ends_with___test_py() -> (
    None
):
    """parse_funtion_module_and_class_from_filename() returns None on filename ends with '__test.py'."""

    assert (
        parse_funtion_module_and_class_from_filename("applications__Air__page__test.py")
        is None
    )


@pytest.mark.solo
def test_parse_funtion_module_and_class_from_filename_returns_None_on_filename_ends_with___init_py() -> (
    None
):
    """parse_funtion_module_and_class_from_filename() returns None on filename is '__init__.py'."""

    assert parse_funtion_module_and_class_from_filename("__init__.py") is None


@pytest.mark.solo
@pytest.mark.parametrize(
    "filename",
    [
        "getCallable.js",
        "example.txt",
        "data.json",
        "script.sh",
        "README.md",
    ],
)
def test_parse_funtion_module_and_class_from_filename_returns_None_on_non_python_files(
    filename: str,
) -> None:
    """parse_funtion_module_and_class_from_filename() returns None when filename is not a python file name."""
    assert parse_funtion_module_and_class_from_filename(filename) is None


@pytest.mark.solo
@pytest.mark.parametrize(
    "filename, expected_output",
    [
        ("applications__Air__get.py", ("applications", "Air", "get")),
        ("applications__Air__page.py", ("applications", "Air", "page")),
        ("applications__Air__post.py", ("applications", "Air", "post")),
        (
            "applications__Requests__get_response.py",
            ("applications", "Requests", "get_response"),
        ),
        (
            "applications__Requests__sanitize_data.py",
            ("applications", "Requests", "sanitize_data"),
        ),
    ],
)
def test_parse_funtion_module_and_class_from_filename_returns_a_tuple_of_module_class_and_method(
    filename: str, expected_output: tuple[str, str, str]
) -> None:
    """parse_funtion_module_and_class_from_filename() returns a tuple of (module, class, method) for a valid class method on a module."""

    assert parse_funtion_module_and_class_from_filename(filename) == expected_output


@pytest.mark.solo
@pytest.mark.parametrize(
    "filename, expected_output",
    [
        ("requests__get.py", ("requests", None, "get")),
        ("requests__page.py", ("requests", None, "page")),
        ("requests__post.py", ("requests", None, "post")),
    ],
)
def test_parse_funtion_module_and_class_from_filename_returns_a_tuple_of_module_None_and_function_on_a_module_level_function(
    filename: str, expected_output: tuple[str, str, str]
) -> None:
    """parse_funtion_module_and_class_from_filename() returns a tuple of (module, None, function) for a valid module-level function."""

    assert parse_funtion_module_and_class_from_filename(filename) == expected_output


def run_teardown_function_for_test_update_example_section_returns_True_on_success():
    """Function to call after test_update_example_section_returns_True_on_success() is ran."""

    # NOTE: TODO remove this sleep after unit tests are done
    time.sleep(7)
    subprocess.run(["uv", "run", "scripts/copy_src_example_to_callable.py"], check=True)


@pytest.mark.current
def test_update_example_section_returns_True_on_success() -> None:
    """update_example_section() returns True on success."""
    from src.air.applications import Air

    new_example_content = """
    import air

    app = air.Air()


    @app.page
    def home():  # routes is "/"
        return air.H1("This is the home page")


    @app.page
    def contact_us():  # route is /contact-us"
        return air.H1("This is the contact page")

    
    """

    applications_module_path = Path("src/air/applications.py")

    page_method_original_usage_example_file = Path(
        "src_examples/applications__Air__page.py"
    )

    page_method_original_example_content = (
        page_method_original_usage_example_file.read_text()
    )

    original_page_method_docstring = Air.page.__doc__

    assert page_method_original_example_content in original_page_method_docstring
    assert new_example_content not in original_page_method_docstring

    update_result = update_example_section(
        file_path=applications_module_path,
        class_name="Air",
        method_name="page",
        example_content=new_example_content,
    )

    assert update_result is True

    new_page_method_docstring = Air.page.__doc__

    assert page_method_original_example_content not in new_page_method_docstring
    assert new_example_content in new_page_method_docstring

    run_teardown_function_for_test_update_example_section_returns_True_on_success()
