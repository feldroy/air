"""
Air 💨 Tags -> Method usage examples!

This example script highlights the Air tag rendering helpers using SMALL_HTML_SAMPLE and HTML_SAMPLE.
It demonstrates pretty-printing, terminal rendering, and browser preview flows guarded by simple if toggles.
Additional scenarios cover exporting tags to dict/JSON, saving prettified HTML, and inspecting debugging
representations.

Run:
    `just run-py-module examples.tags_render`
"""

from __future__ import annotations

from rich import print

import air
from examples.samples.air_tag_samples import AIR_TAG_SAMPLE, SMALL_AIR_TAG_SAMPLE

if __name__ == "__main__":
    # Print pretty-formatted HTML to the terminal when debugging layouts
    if True:
        SMALL_AIR_TAG_SAMPLE.pretty_print()
    # Print a concise representation of the tag.
    if False:
        print(repr(SMALL_AIR_TAG_SAMPLE))
    # Print a full representation of the tag.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.full_repr())
    # Print the rendered HTML representation of the tag.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.render())
    # Print the rendered HTML representation of the tag.
    if False:
        print(str(SMALL_AIR_TAG_SAMPLE))
    # Print the prettified-formatted rendered HTML representation of the tag.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.pretty_render())
    # Print the compact-formatted rendered HTML representation of the tag.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.compact_render())
    # Compare the sizes of different render formats for the HTML representation of the tag.
    if False:
        compact_size = len(AIR_TAG_SAMPLE.compact_render())
        regular_size = len(AIR_TAG_SAMPLE.render())
        pretty_size = len(AIR_TAG_SAMPLE.pretty_render())
        print(f"{compact_size=}, {regular_size=}, {pretty_size=}")
    # Open the rendered HTML representation of the tag in a browser tab.
    if False:
        AIR_TAG_SAMPLE.render_in_the_browser()
    # Open the prettified-formatted rendered HTML representation of the tag in a browser tab.
    if False:
        AIR_TAG_SAMPLE.pretty_render_in_the_browser()
    # Display the prettified-formatted rendered HTML representation of the tag in a browser tab.
    if False:
        SMALL_AIR_TAG_SAMPLE.pretty_display_in_the_browser()
    # Save the rendered HTML representation of the tag to disk.
    if False:
        AIR_TAG_SAMPLE.save(".html_sample.html")
    # Save the prettified-formatted rendered HTML representation of the tag to disk.
    if False:
        AIR_TAG_SAMPLE.pretty_save(".html_sample.html")
    # Visualize the tag tree as a nicely formatted mapping.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.to_pretty_dict())
    # Serialize the tag to a dict.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.to_dict())
    # Serialize the tag to a JSON string.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.to_json())
    # Serialize the tag to a prettified JSON string.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.to_pretty_json())
    # Reconstruct a tag from a serialized dict.
    if False:
        print(repr(SMALL_AIR_TAG_SAMPLE.from_dict(SMALL_AIR_TAG_SAMPLE.to_dict())))
    # Reconstruct a tag from a serialized JSON string.
    if False:
        print(repr(SMALL_AIR_TAG_SAMPLE.from_json(SMALL_AIR_TAG_SAMPLE.to_json())))
    # Convert this air-tag into the instantiable-formatted representation of the tag.
    if False:
        print(SMALL_AIR_TAG_SAMPLE.to_source())
    # Reconstruct the corresponding air-tag tree from the given HTML content.
    if False:
        html_source = SMALL_AIR_TAG_SAMPLE.pretty_render()
        air.Tag.from_html(html_source).pretty_print()
    # Reconstruct the corresponding air-tag tree from the given HTML content
    # into the instantiable-formatted representation of the tag.
    if False:
        html_source = SMALL_AIR_TAG_SAMPLE.pretty_render()
        print(air.Tag.from_html_to_source(html_source))
    # Display the instantiable-formatted representation of the tag in the console with syntax highlighting.
    if False:
        html_source = AIR_TAG_SAMPLE.pretty_render()
        air.Tag.print_source(html_source)
