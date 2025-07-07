from air import *
from eidos.components.headers import EidosHeaders
from eidos.tags import *
from eidos.utils import get_eidos_static_directory

app = Air()

from fastapi.staticfiles import StaticFiles

# Mount static files for CSS
app.mount("/eidos", StaticFiles(directory=get_eidos_static_directory()), name="eidos")

def layout(*content):
    return Html(
        Head(
            *EidosHeaders(),
            Meta(charset="UTF-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            Title("EidosUI MVP - Semantic Components"),
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
    