#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "mcp>=1.17.0",
#   "playwright>=1.55.0",
# ]
# ///

from mcp.server.fastmcp import FastMCP
from textwrap import dedent
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import subprocess

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
def get_change_size_analysis(branch_name: str) -> str:
    """Analyze if a branch's changes are appropriately sized for a single PR

    Args:
        branch_name: Name of the branch to evaluate against main

    Returns:
        Prompt with git diff data for AI analysis of PR scope
    """
    try:
        diff_result = subprocess.run(
            ["git", "diff", f"main...{branch_name}"],
            capture_output=True,
            text=True,
            check=True
        )
        diff = diff_result.stdout.strip()
        
        return dedent(f"""
            Evaluate PR scope for branch '{branch_name}' against main:

            Code changes:
            ```diff
            {diff}
            ```

            PR Scope Guidelines for Air:
            - Good PR: 1-5 files, focused on single feature/fix/refactor
            - Acceptable: 6-10 files if tightly related changes
            - Too large: >10 files or mixing multiple unrelated concerns

            Assess whether changes should be split into multiple PRs for better review.
            Each PR must independently pass `just qa` and `just test`.
        """).strip()
        
    except subprocess.CalledProcessError as e:
        return f"Error running git diff: {e.stderr}"
    except Exception as e:
        return f"Error analyzing changes: {str(e)}"


# ================================================================================
# TOOLS: Example app testing
# ================================================================================

# Global state for browser and process
_state = {
    "playwright": None,
    "browser": None,
    "page": None,
    "process": None,
    "port": 8005,
    "server_logs": [],
    "console_errors": [],
}

@mcp.tool()
async def start_app(example_file: str, port: int = 8005) -> str:
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
    
    _state.update({
        "server_logs": [],
        "console_errors": [],
        "port": port,
    })

    _state["process"] = await asyncio.create_subprocess_exec(
        "uv", "run", str(example_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await asyncio.sleep(3)

    # Start browser
    _state["playwright"] = await async_playwright().start()
    _state["browser"] = await _state["playwright"].chromium.launch(headless=True)
    _state["page"] = await _state["browser"].new_page()

    def __msg_handler(msg):
        if msg.type in ["error", "warning"]:
            _state["console_errors"].append(f"[{msg.type}] {msg.text}")
    _state["page"].on("console", __msg_handler)

    return f"Started {example_file} on port {port}"


@mcp.tool()
async def stop_app() -> str:
    """Stop the running example app and close browser

    Returns:
        Success message with any captured logs/errors
    """
    result = ["App stopped and browser closed"]

    # Capture server logs
    if _state["process"]:
        _state["process"].terminate()
        try:
            stdout, stderr = await asyncio.wait_for(
                _state["process"].communicate(), timeout=2
            )
            if stdout:
                _state["server_logs"].append(stdout.decode())
            if stderr:
                _state["server_logs"].append(stderr.decode())
        except asyncio.TimeoutError:
            _state["process"].kill()

    if _state["page"]:
        await _state["page"].close()
    if _state["browser"]:
        await _state["browser"].close()
    if _state["playwright"]:
        await _state["playwright"].stop()

    if _state["console_errors"]:
        result.append("Console errors/warnings:\n" + "\n".join(_state["console_errors"]))
    if _state["server_logs"]:
        result.append("Server logs:\n" + "\n".join(_state["server_logs"]))

    # Reset state
    _state.update({
        "playwright": None,
        "browser": None,
        "page": None,
        "process": None,
    })

    return "\n\n".join(result)


@mcp.tool()
async def navigate(route: str) -> str:
    """Navigate to a route in the running app

    Args:
        route: Route to navigate to (e.g., "/", "/tags")

    Returns:
        Page title and URL
    """
    if not _state["page"]:
        return "Error: No app running. Use start_app first."

    await _state["page"].goto(f"http://localhost:{_state['port']}{route}")
    return f"URL: {_state['page'].url}\nTitle: {await _state['page'].title()}"


@mcp.tool()
async def click(selector: str) -> str:
    """Click an element on the current page

    Args:
        selector: CSS selector to click (e.g., "a[href='/tags']", "button.submit")

    Returns:
        Result after clicking (new URL and title)
    """
    if not _state["page"]:
        return "Error: No page loaded. Use start_app and navigate first."

    element = _state["page"].locator(selector)
    if await element.count() == 0:
        return f"Element not found: {selector}"

    await element.first.click()
    await _state["page"].wait_for_load_state()
    return f"Clicked: {selector}\nURL: {_state['page'].url}\nTitle: {await _state['page'].title()}"


@mcp.tool()
async def get_logs() -> str:
    """Get captured server logs and browser console errors

    Returns:
        All captured logs and errors
    """
    result = []

    if _state["process"] and _state["process"].returncode is None:
        result.append("Server is running (logs available on stop_app)")

    if _state["console_errors"]:
        result.append("Console errors/warnings:\n" + "\n".join(_state["console_errors"]))
    else:
        result.append("No console errors")

    if _state["server_logs"]:
        result.append("Server logs:\n" + "\n".join(_state["server_logs"]))

    return "\n\n".join(result) if result else "No logs captured yet"

if __name__ == "__main__":
    mcp.run()