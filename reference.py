import importlib
from functools import cache
import importlib
import inspect
import pkgutil
from typing import Any, List, ParamSpec,TypeVar, Callable

import air
from air_markdown.tags import AirMarkdown

app = air.Air()

renderer = air.JinjaRenderer("templates")


def layout(request: air.Request, *content):
    if not isinstance(request, air.Request):
        raise Exception("First arg of layout needs to be an air.Request")
    head_tags = air.layouts.filter_head_tags(content)
    body_tags = air.layouts.filter_body_tags(content)
    return renderer(
        request,
        "page.html",
        head_tags=air.Children(*head_tags),
        body_tags=air.Children(*body_tags),
    )



@cache
def _get_air_objects() -> List[Any]:
    """
    Gets all the objects in the `air` package that are defined within air
    (nothing imported into air from core python or other libraries).

    Returns:
        A list of these objects.
    """
    air_objects = set()
    prefix = air.__name__ + "."
    for _, module_name, _ in pkgutil.walk_packages(air.__path__, prefix):
        try:
            module = importlib.import_module(module_name)
            for _, obj in inspect.getmembers(module):
                if hasattr(obj, "__module__") and obj.__module__.startswith(
                    air.__name__
                ):
                    air_objects.add(obj)
        except Exception:
            continue
    return list(air_objects)


reference_warning = air.Section(
                air.P(
                    air.Strong("WARNING:", style="color: red"),
                    " This API reference is very new and there may be formatting challenges.",
                    style="color: red"
                )
            )


@app.page
async def index(request: air.Request):
    modules = [
        air.Li(air.A(x, href=f"/reference/{x}"))
        for x in sorted(list(set([x.__module__ for x in _get_air_objects()])))
    ]
    return layout(
        request, air.Article(air.H1("API Reference"), reference_warning, air.Ul(*modules), class_="prose")
    )


def _callable_kwargs_to_markdown(func: Callable) -> str:
    """
    Generate a Markdown table of a callable's arguments (positional + keyword).
    
    Columns:
    - Name
    - Type
    - Default
    - Description (from docstring Args section if available)
    """
    sig = inspect.signature(func)
    headers = ["Name", "Type", "Default", "Description"]
    rows = []

    # --- Parse docstring for argument descriptions ---
    doc = inspect.getdoc(func) or ""
    arg_descriptions = {}
    in_args_section = False
    for line in doc.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("args:"):
            in_args_section = True
            continue
        if in_args_section:
            if not stripped:  # blank line ends section
                break
            if ":" in stripped:
                name, desc = stripped.split(":", 1)
                arg_descriptions[name.strip()] = desc.strip()

    # --- Build table rows ---
    for name, param in sig.parameters.items():
        if name == 'kwargs': continue
        # Argument type
        if param.annotation is not inspect.Parameter.empty:
            arg_type = getattr(param.annotation, "__name__", str(param.annotation))
        else:
            arg_type = "Any"

        # Default value
        if param.default is not inspect.Parameter.empty:
            default = repr(param.default)
        else:
            default = "No default"

        # Description from docstring
        desc = arg_descriptions.get(name, "")

        rows.append([name, arg_type, default, desc])

    # --- Build markdown table ---
    md = f"| {' | '.join(headers)} |\n"
    md += f"| {' | '.join(['---']*len(headers))} |\n"
    for row in rows:
        md += f"| {' | '.join(row)} |\n"

    return md

def _remove_args_section(docstring: str) -> str:
    """
    Remove the 'Args:' section (and its contents) from a docstring string.
    """
    if not docstring:
        return docstring

    lines = docstring.splitlines()
    cleaned = []
    in_args_section = False

    for line in lines:
        stripped = line.strip()

        # Detect start of Args section
        if stripped.lower().startswith("args:"):
            in_args_section = True
            continue

        if in_args_section:
            # Stop skipping if we hit a non-indented line or a blank line
            if stripped == "" or not line.startswith((" ", "\t")):
                in_args_section = False
                cleaned.append(line)
            # else: keep skipping arg lines
        else:
            cleaned.append(line)

    return "\n".join(cleaned)



def doc_obj(obj):
    doc = _callable_kwargs_to_markdown(obj)
    doc += '\n\n'
    raw_doc = obj.__doc__ if (hasattr(obj, "__doc__") and isinstance(obj.__doc__, str)) else ""    
    doc += _remove_args_section(raw_doc)
    return air.Section(
        air.H2(obj.__name__, air.Small(f"  ({obj.__module__}.{obj.__name__})")),
        AirMarkdown(doc)
    )


@app.get("/{module_name:path}")
def reference_module(request: air.Request, module_name: str):
    module = importlib.import_module(module_name)
    objects = [
        x
        for x in _get_air_objects()
        if x.__module__ == module_name and not isinstance(x, (ParamSpec, TypeVar)) and not x.__name__.startswith('_')
    ]
    objects = [doc_obj(x) for x in sorted(objects, key=lambda x: x.__name__)]
    return layout(
        request,
        air.Article(
            air.H1(air.A("API Reference:", href="/reference"), " ", module_name),
            reference_warning,
            AirMarkdown(module.__doc__ if module.__doc__ is not None else ''),
            air.Ul(*objects),
            class_="prose",
        ),
    )