"""
Air 💨 Tags -> Method usage examples!

This example script highlights the Air tag rendering helpers using SMALL_HTML_SAMPLE and HTML_SAMPLE.
It demonstrates pretty-printing, terminal rendering, and browser preview flows guarded by simple if toggles.
Additional scenarios cover exporting tags to dict/JSON, saving prettified HTML, and inspecting debugging representations.

Run:
    `just run-py-module examples.tags_render`
"""

from __future__ import annotations

from rich import print

from examples.html_sample import HTML_SAMPLE, SMALL_HTML_SAMPLE

if __name__ == "__main__":
    # Print pretty-formatted HTML to the terminal when debugging layouts
    if True:
        SMALL_HTML_SAMPLE.pretty_print()
    # Print a concise representation of the tag.
    if False:
        print(repr(SMALL_HTML_SAMPLE))
    # Print a full representation of the tag.
    if False:
        print(SMALL_HTML_SAMPLE.full_repr())
    # Print the rendered HTML representation of the tag.
    if False:
        print(SMALL_HTML_SAMPLE.render())
    # Print the rendered HTML representation of the tag.
    if False:
        print(str(SMALL_HTML_SAMPLE))
    # Print the prettified-formatted rendered HTML representation of the tag.
    if False:
        print(SMALL_HTML_SAMPLE.pretty_render())
    # Open the rendered HTML representation of the tag in a browser tab.
    if False:
        HTML_SAMPLE.render_in_the_browser()
    # Open the prettified-formatted rendered HTML representation of the tag in a browser tab.
    if False:
        HTML_SAMPLE.pretty_render_in_the_browser()
    # Display the prettified-formatted rendered HTML representation of the tag in a browser tab.
    if False:
        SMALL_HTML_SAMPLE.pretty_display_in_the_browser()
    # Save the rendered HTML representation of the tag to disk.
    if False:
        HTML_SAMPLE.save(".html_sample.html")
    # Save the prettified-formatted rendered HTML representation of the tag to disk.
    if False:
        HTML_SAMPLE.pretty_save(".html_sample.html")
    # Visualize the tag tree as a nicely formatted mapping.
    if False:
        print(SMALL_HTML_SAMPLE.to_pretty_dict())
    # Serialize the tag to a dict.
    if False:
        print(SMALL_HTML_SAMPLE.to_dict())
    # Serialize the tag to a JSON string.
    if False:
        print(SMALL_HTML_SAMPLE.to_json())
    # Serialize the tag to a prettified JSON string.
    if False:
        print(SMALL_HTML_SAMPLE.to_pretty_json())
    # Reconstruct a tag from a serialized dict.
    if False:
        print(repr(SMALL_HTML_SAMPLE.from_dict(SMALL_HTML_SAMPLE.to_dict())))
    # Reconstruct a tag from a serialized JSON string.
    if False:
        print(repr(SMALL_HTML_SAMPLE.from_json(SMALL_HTML_SAMPLE.to_json())))
