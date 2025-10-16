#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mcp>=1.17.0",
#   "playwright>=1.40.0",
# ]
# ///

from mcp.server.fastmcp import FastMCP
from textwrap import dedent
from subprocess import Popen, PIPE
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

# Create the MCP server
mcp = FastMCP(
    name="Air Contributions",
    dependencies=["mcp>=1.17.0"]
)

@mcp.resource('quality://code_quality_prompt')
def get_code_quality_prompt() -> str:
    """Get the code quality standards prompt for Air contributions"""
    return dedent("""
        Review code changes for adherence to Air project standards:

        - All new features must include tests and docstrings
        - Use Google-style docstrings for all public functions/classes/methods
        - Ensure `just qa` passes (Ruff formatting/linting, Ty/Pyrefly type checking)
        - Ensure `just test` passes (pytest with 95% coverage requirement)
        - Follow conventional commits format: <type>(<scope>): <description>
        - Keep changes focused and small (single responsibility per PR)
        - Use Python 3.13+ type hints with proper annotations
        - Prefer editing existing files over creating new ones
        - Line length: 120 characters max
        - Use double quotes for strings
    """).strip()

@mcp.tool()
def get_change_size_prompt(branch_name: str) -> str:
    """Evaluate if a branch's changes are appropriately sized for a single PR

    Args:
        branch_name: Name of the branch to evaluate against main

    Returns:
        Prompt with guidelines for evaluating PR scope
    """
    return dedent(f"""
        Evaluate PR scope for branch '{branch_name}' against main:

        Run: `git diff main...{branch_name} --stat` and `git diff main...{branch_name} --name-only`

        PR Scope Guidelines for Air:
        - Good PR: 1-5 files, focused on single feature/fix/refactor
        - Acceptable: 6-10 files if tightly related changes
        - Too large: >10 files or mixing multiple unrelated concerns

        Assess whether changes should be split into multiple PRs for better review.
        Each PR must independently pass `just qa` and `just test`.
    """).strip()


# ================================================================================
# TOOLS: Example app testing
# ================================================================================

# Global state for browser and process
__state = {
    "playwright": None,
    "browser": None,
    "page": None,
    "process": None,
    "port": 8005,
    "server_logs": [],
    "console_errors": [],
}

@mcp.tool()
def start_app(example_file: str, port: int = 8005) -> str:
    """Start an Air example app from the `examples/` directory

    Args:
        example_file: Name of the example file (e.g., "airblog.py")
        port: Port to run on (default: 8005)

    Returns:
        Success message or error
    """
    example_path = Path("examples") / example_file
    if not example_path.exists():
        return f"Error: {example_file} not found in examples/"
    
    __state.update({
        "server_logs": [],
        "console_errors": [],
        "port": port,
    })

    # Start app
    __state["process"] = Popen(["uv", "run", str(example_path)], stdout=PIPE, stderr=PIPE, text=True)
    time.sleep(3)

    # Start browser
    __state["playwright"] = sync_playwright().start()
    __state["browser"] = __state["playwright"].chromium.launch(headless=True)
    __state["page"] = __state["browser"].new_page()

    # Capture console errors
    __state["page"].on("console", lambda msg:
        __state["console_errors"].append(f"[{msg.type}] {msg.text}")
        if msg.type in ["error", "warning"] else None
    )

    return f"Started {example_file} on port {port}"


@mcp.tool()
def stop_app() -> str:
    """Stop the running example app and close browser

    Returns:
        Success message with any captured logs/errors
    """
    result = ["App stopped and browser closed"]

    # Capture server logs
    if __state["process"]:
        __state["process"].terminate()
        stdout, stderr = __state["process"].communicate(timeout=2)
        if stdout:
            __state["server_logs"].append(stdout)
        if stderr:
            __state["server_logs"].append(stderr)

    # Close browser
    if __state["page"]:
        __state["page"].close()
    if __state["browser"]:
        __state["browser"].close()
    if __state["playwright"]:
        __state["playwright"].stop()

    # Report errors and logs
    if __state["console_errors"]:
        result.append("Console errors/warnings:\n" + "\n".join(__state["console_errors"]))
    if __state["server_logs"]:
        result.append("Server logs:\n" + "\n".join(__state["server_logs"]))

    # Reset state
    __state.update({
        "playwright": None,
        "browser": None,
        "page": None,
        "process": None,
    })

    return "\n\n".join(result)


@mcp.tool()
def navigate(route: str) -> str:
    """Navigate to a route in the running app

    Args:
        route: Route to navigate to (e.g., "/", "/tags")

    Returns:
        Page title and URL
    """
    if not __state["page"]:
        return "Error: No app running. Use start_app first."

    __state["page"].goto(f"http://localhost:{__state['port']}{route}")
    return f"URL: {__state['page'].url}\nTitle: {__state['page'].title()}"


@mcp.tool()
def click(selector: str) -> str:
    """Click an element on the current page

    Args:
        selector: CSS selector to click (e.g., "a[href='/tags']", "button.submit")

    Returns:
        Result after clicking (new URL and title)
    """
    if not __state["page"]:
        return "Error: No page loaded. Use start_app and navigate first."

    element = __state["page"].locator(selector)
    if element.count() == 0:
        return f"Element not found: {selector}"

    element.first.click()
    __state["page"].wait_for_load_state()
    return f"Clicked: {selector}\nURL: {__state['page'].url}\nTitle: {__state['page'].title()}"


@mcp.tool()
def get_logs() -> str:
    """Get captured server logs and browser console errors

    Returns:
        All captured logs and errors
    """
    result = []

    if __state["process"] and __state["process"].poll() is None:
        result.append("Server is running (logs available on stop_app)")

    if __state["console_errors"]:
        result.append("Console errors/warnings:\n" + "\n".join(__state["console_errors"]))
    else:
        result.append("No console errors")

    if __state["server_logs"]:
        result.append("Server logs:\n" + "\n".join(__state["server_logs"]))

    return "\n\n".join(result) if result else "No logs captured yet"



# ================================================================================
# SERVER STARTUP
# ================================================================================

if __name__ == "__main__":
    mcp.run()