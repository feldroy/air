from air import *
from eidos.tags import *

app = Air()

from fastapi.staticfiles import StaticFiles
import os

# Mount static files for CSS
app.mount("/eidos", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "eidosui")), name="eidos")

def layout(*content):
    return Html(
        Head(
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("EidosUI MVP - Semantic Components"),
            Script(src="https://cdn.tailwindcss.com"),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/gh/kentro-tech/EidosUI@main/eidos/css/styles.css"),
            Link(rel="stylesheet", href="/eidos/css/themes/eidos-variables.css"),
            Link(rel="stylesheet", href="/eidos/css/themes/light.css"),
            Link(rel="stylesheet", href="/eidos/css/themes/dark.css")
            ),
        Body(
            Main(
                    Button("🌙", id="theme-toggle", cls="fixed top-4 right-4 p-2 rounded-full bg-gray-200 dark:bg-gray-800"),
                    *content,
                    cls='p-12'
            ),
            Script("""
                const toggle = document.getElementById('theme-toggle');
                toggle.addEventListener('click', () => {
                    const html = document.documentElement;
                    const currentTheme = html.getAttribute('data-theme');
                    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                    html.setAttribute('data-theme', newTheme);
                    toggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
                });
            """)
                )
        )    


@app.get('/')
def index():
    return layout(H1('Hello, World'))
    