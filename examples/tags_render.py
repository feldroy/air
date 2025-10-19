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
    # Render the full HTML document when serializing the response body
    if False:
        print(SMALL_HTML_SAMPLE.render()[:80])
    # Open the rendered HTML in a browser tab while previewing changes locally
    if False:
        HTML_SAMPLE.render_in_the_browser()
    # Launch a prettified HTML preview in the browser for design reviews
    if False:
        HTML_SAMPLE.pretty_render_in_the_browser()
    # Produce a formatted HTML string with a body wrapper for documentation snippets
    if False:
        print(SMALL_HTML_SAMPLE.pretty_render(with_body=True)[:80])
    # Save the rendered HTML to disk for static hosting hand-off
    if False:
        HTML_SAMPLE.save(".html_sample.html")
    # Persist a human-readable HTML file with indentation for code reviews
    if False:
        HTML_SAMPLE.pretty_save(".html_sample.html")
    # Display formatted HTML in the browser when sharing review links
    if False:
        SMALL_HTML_SAMPLE.pretty_display_in_the_browser()
    # Leverage __str__ to embed the tag in string contexts automatically
    if False:
        print(str(SMALL_HTML_SAMPLE)[:80])
    # Inspect the concise debug representation for logging purposes
    if False:
        print(repr(SMALL_HTML_SAMPLE))
    # Review the full tag hierarchy for quick debugging of nested structures
    if False:
        print(SMALL_HTML_SAMPLE.full_repr())
    # Visualize the tag tree as a nicely formatted mapping for debugging
    if False:
        print(SMALL_HTML_SAMPLE.to_pretty_dict())
    # Serialize the tag to a dict for JSON responses or caching
    if False:
        print(SMALL_HTML_SAMPLE.to_dict())
    # Convert child nodes into serializable values for storage
    if False:
        print(SMALL_HTML_SAMPLE.to_child_dict())
    # Export the tag tree as JSON for API payloads
    if False:
        print(SMALL_HTML_SAMPLE.to_json(indent=2))
    # Generate a prettified JSON string for human inspection
    if False:
        print(SMALL_HTML_SAMPLE.to_pretty_json())
    # Rebuild a tag hierarchy from serialized dict data during hydration
    if False:
        print(repr(SMALL_HTML_SAMPLE.from_dict(SMALL_HTML_SAMPLE.to_dict())))
    # Hydrate a tag tree directly from its JSON representation
    if False:
        print(repr(SMALL_HTML_SAMPLE.from_json(SMALL_HTML_SAMPLE.to_json()).render()))
