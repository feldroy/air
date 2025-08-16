import air
from rich import print


def test_css_render_from_init():
    vars = air.css.CSSVariables(
        font_primary= """'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif""",

        # Modern Color System
        color_slate_50= "#f8fafc",
        color_slate_100= "#f1f5f9",
        color_slate_200= "#e2e8f0",
    )    
    css = vars.render()

    assert css == ''




class Theme(air.css.CSSVariables):
    font_primary= """'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"""

    # Modern Color System
    color_slate_50= "#f8fafc"
    color_slate_100= "#f1f5f9"
    color_slate_200= "#e2e8f0"
    color_slate_300= "#cbd5e1"
    color_slate_400= "#94a3b8"
    color_slate_500= "#64748b"
    color_slate_600= "#475569"
    color_slate_700= "#334155"
    color_slate_800= "#1e293b"
    color_slate_900= "#0f172a"
    color_primary=    "#6366f1"
    color_primary_50= "#eef2ff"

    color_primary_100= "#e0e7ff"
    color_primary_500= "#6366f1"
    color_primary_600= "#5b21b6"
    color_primary_700= "#4c1d95"
    color_primary_900= "#312e81"
    color_secondary=    "#06b6d4"
    color_secondary_50= "#ecfeff"
    color_secondary_100= "#cffafe"
    color_secondary_500= "#06b6d4"
    color_secondary_600= "#0891b2"
    color_secondary_700= "#0e7490"    


vars = air.css.CSSVariables(
    font_primary= """'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif""",

    # Modern Color System
    color_slate_50= "#f8fafc",
    color_slate_100= "#f1f5f9",
    color_slate_200= "#e2e8f0",
    color_slate_300= "#cbd5e1",
    color_slate_400= "#94a3b8",
    color_slate_500= "#64748b",
    color_slate_600= "#475569",
    color_slate_700= "#334155",
    color_slate_800= "#1e293b",
    color_slate_900= "#0f172a",
    color_primary=    "#6366f1",
    color_primary_50= "#eef2ff",
    color_primary_100= "#e0e7ff",
    color_primary_500= "#6366f1",
    color_primary_600= "#5b21b6",
    color_primary_700= "#4c1d95",
    color_primary_900= "#312e81",
    color_secondary=    "#06b6d4",
    color_secondary_50= "#ecfeff",
    color_secondary_100= "#cffafe",
    color_secondary_500= "#06b6d4",
    color_secondary_600= "#0891b2",
    color_secondary_700= "#0e7490"        ,
)

# color_secondary = StepColorPalette(["06b6d4", "ecfeff", "cffafe"])
color_secondary = {50: "06b6d4", 100: "ecfeff", 500: "cffafe"}    