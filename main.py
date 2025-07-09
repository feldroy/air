import air
from eidos.components.headers import EidosHeaders
import eidos.tags as et
from eidos.utils import get_eidos_static_directory

app = air.Air()

from fastapi.staticfiles import StaticFiles

# Mount static files for CSS
app.mount("/eidos", StaticFiles(directory=get_eidos_static_directory()), name="eidos")

def layout(*content):
    head_tags = air.layouts.filter_head_tags(content)
    body_tags = air.layouts.filter_body_tags(content)
    return air.Html(
        air.Head(
            *EidosHeaders(),
            air.Meta(charset="UTF-8"),
            air.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            *head_tags
            ),
        et.Body(
            air.Main(
                    et.Button("🌙", id="theme-toggle", cls="fixed top-4 right-4 p-2 rounded-full bg-gray-200 dark:bg-gray-800"),
                    *body_tags,
                    cls='p-12'
            ),
            air.Script("""
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
    return layout(
        air.Title('Hello, world'),
        et.H1('Hello, World'))
    