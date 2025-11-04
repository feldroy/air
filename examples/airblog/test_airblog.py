"""
Minimal tests for airblog.py - demonstrating different test types.
"""

import pytest
import uvicorn
import multiprocessing
import time
from starlette.testclient import TestClient
from playwright.sync_api import Page, expect

from airblog import app, get_article
import socket

def get_free_port() -> int:
    """
    Finds a free port on localhost for the live server.  
    
    This is only neccesary for parallel end to end tests to avoid port conflicts.
    """
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def run_server(port_queue):
    "Runs the AirBlog server on a free port and communicates the port back via a queue."
    # Get an available port number from the operating system
    port = get_free_port()
    
    # Send the port number back to the parent process via the queue
    # This allows the test to know which port the server is running on
    port_queue.put(port)
    
    # Start the uvicorn server on the allocated port
    uvicorn.run("airblog:app", host="127.0.0.1", port=port, log_level="error")

@pytest.fixture(scope="function")
def live_server():
    """
    A generator function that starts a live server in a separate process.

    This function creates a multiprocessing queue to communicate the port 
    number on which the server is running. It starts the server process, 
    waits for the port to be available, and yields the port number for 
    use in tests. After the tests are done, it terminates the server 
    process and ensures it has finished executing.

    Yields:
        int: The port number on which the live server is running.
    """
    port_queue = multiprocessing.Queue()
    server = multiprocessing.Process(target=run_server, args=(port_queue,))
    server.start()
    port = port_queue.get(timeout=5)
    time.sleep(2)
    yield port
    server.terminate()
    server.join()


# UNIT TEST - Tests a single function in isolation
def test_get_article_returns_article():
    article = get_article("hello-world")
    assert article is not None
    assert "Daniel" in article['frontmatter']
    assert article["attributes"]["slug"] == "hello-world"


# INTEGRATION TEST - Tests route handler with Air app
def test_index_route_renders():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert "AirBlog!" in response.text
        assert "<small>2025-09-26</small>" in response.text


# END-TO-END TEST - Tests full application flow with real browser
def test_navigate_to_article_via_click(page: Page, live_server):
    page.goto(f"http://localhost:{live_server}")
    page.click("text=Hello World")
    expect(page).to_have_url(f"http://localhost:{live_server}/article/hello-world")
    expect(page.locator("h1")).to_contain_text("Hello World")


# ACCESSIBILITY TEST - Verifies proper semantic structure
def test_page_accessibility(page: Page, live_server):
    page.goto(f"http://localhost:{live_server}")
    expect(page.locator("h1")).to_be_visible()
    expect(page.locator("nav")).to_be_visible()
    expect(page.locator("header")).to_be_visible()

