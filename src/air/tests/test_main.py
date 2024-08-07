import os
import shutil
import pytest
from air import main

def test_main():
    assert main() == 0

def test_fasthtml_plugin():
    # Setup: create a temporary input directory with a FastHTML app
    input_dir = "input"
    output_dir = "public"
    os.makedirs(input_dir, exist_ok=True)
    with open(os.path.join(input_dir, "hello_fasthtml.py"), "w") as f:
        f.write("""
from fasthtml.common import *

app, rt = fast_app()

@rt('/')
def get():
    return Div(P("Hello, FastHTML!"))

serve()
        """)

    # Run the main function to build the site
    main()

    # Check if the HTML file was generated correctly
    output_file = os.path.join(output_dir, "index.html")
    assert os.path.exists(output_file)
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "<p>Hello, FastHTML!</p>" in content

    # Cleanup
    shutil.rmtree(input_dir)
    shutil.rmtree(output_dir)
