from inspect import cleandoc
from typing import Final

FRAGMENT_AIR_TAG_SOURCE_SAMPLE: Final = cleandoc(
    """
    air.Div(
        air.Meta(charset='utf-8'),
        air.Meta(
            content='width=device-width,initial-scale=1',
            name='viewport',
        ),
        air.Title('Title!'),
        air.Comment('My crazy comment'),
        air.P(
            'Hello',
            air.Strong('World'),
            '!',
        ),
    )
    """
)

TINY_AIR_TAG_SOURCE_SAMPLE: Final = cleandoc(
    """
    air.Html(
        air.Head(
            air.Meta(charset='utf-8'),
            air.Meta(
                content='width=device-width,initial-scale=1',
                name='viewport',
            ),
            air.Title('Title!'),
            air.Comment('My crazy comment'),
        ),
        air.Body(
            air.P(
                'Hello',
                air.Strong('World'),
                '!',
            ),
            air.Div(
                'Div',
                hidden=True,
                draggable=True,
                translate='no',
                contenteditable=True,
                tabindex=3,
                width=12.34,
            ),
        ),
        lang='en',
    )
    """
)

SMALL_AIR_TAG_SOURCE_SAMPLE: Final = cleandoc(
    """
    air.Html(
        air.Head(),
        air.Body(
            air.Div(
                air.Link(
                    href='https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css',
                    rel='stylesheet',
                ),
                air.Script(
                    src='https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js',
                    crossorigin='anonymous',
                    integrity='sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm',
                ),
                air.H1(
                    'H1',
                    data_cloud=True,
                    data_earth='true',
                ),
                air.H2(
                    'H1',
                    data_cloud=True,
                    data_earth='true',
                ),
                air.P(
                    air.A(
                        'A',
                        data_cloud=True,
                        data_earth='true',
                    ),
                    air.A(':root & > < { --pico-font-size: 100%; }', id_='id1'),
                    'safe <> string',
                    air.A(':root & > < { --pico-font-size: 100%; }', id_='id1'),
                    air.Img(
                        selected=True,
                        bar='foo',
                        src='https://cdn.jsdelivr.net/dist/img.png',
                        width=250,
                        height=100,
                        alt='My Img',
                    ),
                    '<>',
                    air.Script('safe <> Script', crossorigin='anonymous'),
                ),
                kwarg1='kwarg1',
                kwarg2='kwarg2',
                kwarg3='kwarg3',
                class_='class1',
                id_='id1',
                style='style1',
            ),
        ),
    )
    """
)

AIR_TAG_SOURCE_SAMPLE: Final = cleandoc(
    """
    air.Html(
        air.Head(
            air.Meta(
                property='og:image',
                content='https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg',
            ),
            air.Meta(
                property='og:site_name',
                content='https://daniel.feldroy.com',
            ),
            air.Meta(
                property='og:image:type',
                content='image/png',
            ),
            air.Meta(
                property='og:type',
                content='website',
            ),
            air.Meta(
                property='og:url',
                content='http://daniel.feldroy.com/',
            ),
            air.Meta(
                property='og:title',
                content='Daniel Roy Greenfeld',
            ),
            air.Meta(
                property='og:description',
                content="Daniel Roy Greenfeld's personal blog",
            ),
            air.Meta(
                content='https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg',
                name='twitter:image',
            ),
            air.Meta(
                content='summary',
                name='twitter:card',
            ),
            air.Meta(
                content='Daniel Roy Greenfeld',
                name='twitter:title',
            ),
            air.Meta(
                content="Daniel Roy Greenfeld's personal blog",
                name='twitter:description',
            ),
            air.Link(
                href='http://daniel.feldroy.com/',
                rel='canonical',
            ),
            air.Link(
                href='https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css',
                rel='stylesheet',
            ),
            air.Script(
                src='https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js',
                crossorigin='anonymous',
                integrity='sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm',
            ),
            air.Style(':root { --pico-font-size: 100%; }'),
            air.Link(
                href='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-dark.css',
                media='(prefers-color-scheme: dark)',
                rel='stylesheet',
            ),
            air.Link(
                href='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-light.css',
                media='(prefers-color-scheme: light)',
                rel='stylesheet',
            ),
            air.Script(src='https://cdn.jsdelivr.net/npm/marked/marked.min.js'),
            air.Script(src='https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js'),
            air.Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/python.min.js'),
            air.Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/javascript.min.js'),
            air.Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/html.min.js'),
            air.Script(src='https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/css.min.js'),
            air.Link(
                href='/public/style.css',
                rel='stylesheet',
                type='text/css',
            ),
            air.Title('Daniel Roy Greenfeld'),
        ),
        air.Body(
            air.Header(
                air.A(
                    air.Img(
                        src='https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg',
                        width='108',
                        alt='Daniel Roy Greenfeld',
                        class_='borderCircle',
                    ),
                    href='/',
                ),
                air.A(
                    air.H2('Daniel Roy Greenfeld'),
                    href='/',
                ),
                air.P(
                    air.A('About', href='/about'),
                    '|',
                    air.A('Articles (715)', href='/posts'),
                    '|',
                    air.A('Books', href='/books'),
                    '|',
                    air.A('Jobs', href='/jobs'),
                    '|',
                    air.A('Tags', href='/tags'),
                    '|',
                    air.A('Search', href='/search'),
                ),
                style='text-align: center;',
            ),
            air.Main(
                air.Div(
                    air.Section(
                        air.H1('Recent Writings'),
                        air.Span(
                            air.H2(
                                air.A('Unpack for keyword arguments', href='/posts/2025-07-unpack-for-keyword-arguments'),
                            ),
                            air.P(
                                'Keyword arguments can now be more narrowly typed by using typing.Unpack and typing.TypeDict.',
                                air.Br(),
                                air.Small(
                                    air.Time('July 27, 2025 at 4:55pm'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H2(
                                air.A('uv run for running tests on versions of Python', href='/posts/2025-07-uv-run-for-testing-python-versions'),
                            ),
                            air.P(
                                'Using uv run with make to replace tox or nox for testing multiple versions of Python locally.',
                                air.Br(),
                                air.Small(
                                    air.Time('July 20, 2025 at 10:08am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H2(
                                air.A('Farewell to Michael Ryabushkin', href='/posts/2025-05-farewell-to-michael-ryabushkin'),
                            ),
                            air.P(
                                'In early May of 2025 Michael Ryabushkin (aka Goodwill) passed away. He was a great friend and an even better person. I will miss him dearly.',
                                air.Br(),
                                air.Small(
                                    air.Time('May 16, 2025 at 11:22am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H2(
                                air.A('Exploring flexicache', href='/posts/2025-05-flexicache'),
                            ),
                            air.P(
                                'An exploration of using flexicache for caching in Python.',
                                air.Br(),
                                air.Small(
                                    air.Time('May 09, 2025 at 8:00am'),
                                ),
                            ),
                        ),
                        air.P(
                            air.A('Read all articles', href='<function posts at 0x7fa78cb1b740>'),
                        ),
                    ),
                    air.Section(
                        air.H1(
                            'TIL',
                            air.Small('(Today I learned)'),
                        ),
                        air.Span(
                            air.H3(
                                air.A('Setting environment variables for pytest', href='/posts/til-2025-09-setting-environment-variables-for-pytest'),
                            ),
                            air.P(
                                air.Small(
                                    air.Time('September 02, 2025 at 2:29am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H3(
                                air.A('Using SQLModel Asynchronously with FastAPI (and Air) with PostgreSQL', href='/posts/til-2025-08-using-sqlmodel-asynchronously-with-fastapi-and-air-with-postgresql'),
                            ),
                            air.P(
                                air.Small(
                                    air.Time('August 29, 2025 at 5:54am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H3(
                                air.A('Single source version package builds with uv (redux)', href='/posts/til-2025-08-single-source-version-package-builds-with-uv-redux'),
                            ),
                            air.P(
                                air.Small(
                                    air.Time('August 22, 2025 at 2:20am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H3(
                                air.A('How to type args and kwargs', href='/posts/til-2025-07-how-to-type-args-and-kwargs'),
                            ),
                            air.P(
                                air.Small(
                                    air.Time('July 26, 2025 at 9:15am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H3(
                                air.A('Single source version package builds with uv', href='/posts/til-2025-07-single-source-version-package-builds-with-uv'),
                            ),
                            air.P(
                                air.Small(
                                    air.Time('July 23, 2025 at 1:59am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H3(
                                air.A('Removing exif geodata from media', href='/posts/til-2025-06-removing-exif-geodata-from-media'),
                            ),
                            air.P(
                                air.Small(
                                    air.Time('June 23, 2025 at 8:56pm'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H3(
                                air.A('HTML 404 errors for FastAPI', href='/posts/til-2025-06-html-404-errors-for-fastapi'),
                            ),
                            air.P(
                                air.Small(
                                    air.Time('June 13, 2025 at 4:23am'),
                                ),
                            ),
                        ),
                        air.P(
                            air.A('Read more TIL articles', href='/tags/TIL'),
                        ),
                    ),
                    air.Section(
                        air.H1('Featured Writings'),
                        air.Span(
                            air.H2(
                                air.A('The Thirty Minute Rule', href='/posts/thirty-minute-rule'),
                            ),
                            air.P(
                                'What to do when you get stuck on a coding issue for more than 30 minutes.',
                                air.Br(),
                                air.Small(
                                    air.Time('August 18, 2021 at 12:00am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H2(
                                air.A("What's the Best Thing about Working for Octopus Energy?", href='/posts/whats-the-best-thing-about-working-for-octopus-energy-part-1'),
                            ),
                            air.P(
                                'An in-depth discussion about my employment at Octopus Energy.',
                                air.Br(),
                                air.Small(
                                    air.Time('June 08, 2021 at 11:59pm'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H2(
                                air.A('Code, Code, Code', href='/posts/code-code-code'),
                            ),
                            air.P(
                                "I'm often asked by new programmers how they can forge a path into using their skills professionally. Or how they can get better at writing software. In this article I share the secret master-level method to improvement.",
                                air.Br(),
                                air.Small(
                                    air.Time('May 28, 2016 at 12:00am'),
                                ),
                            ),
                        ),
                        air.Span(
                            air.H2(
                                air.A('I Married Audrey Roy', href='/posts/i-married-audrey-roy'),
                            ),
                            air.P(
                                'The story of one of the best days of my life.',
                                air.Br(),
                                air.Small(
                                    air.Time('January 04, 2014 at 12:00am'),
                                ),
                            ),
                        ),
                    ),
                    class_='grid',
                ),
                class_='container',
            ),
            air.Footer(
                air.Hr(),
                air.P(
                    air.A(
                        'LinkedIn',
                        href='https://www.linkedin.com/in/danielfeldroy/',
                        target='_blank',
                    ),
                    '|',
                    air.A(
                        'Bluesky',
                        href='https://bsky.app/profile/daniel.feldroy.com',
                        target='_blank',
                    ),
                    '|',
                    air.A(
                        'Twitter',
                        href='https://twitter.com/pydanny',
                        target='_blank',
                    ),
                    '|',
                    air.A(
                        'Github',
                        href='https://github.com/pydanny',
                        target='_blank',
                    ),
                    '| Feeds:',
                    air.A(
                        'All',
                        href='/feeds/atom.xml',
                        target='_blank',
                    ),
                    ',',
                    air.A(
                        'Python',
                        href='/feeds/python.atom.xml',
                        target='_blank',
                    ),
                    ',',
                    air.A(
                        'TIL',
                        href='/feeds/til.atom.xml',
                        target='_blank',
                    ),
                ),
                air.P('All rights reserved 2025, Daniel Roy Greenfeld'),
                class_='container',
            ),
            air.Dialog(
                air.Header(
                    air.H2('Search'),
                    air.Input(
                        hx_trigger='keyup',
                        hx_get='/search-results',
                        hx_target='.search-results-modal',
                        name='q',
                        type='text',
                        placeholder='Enter your search query...',
                        id_='search-input',
                    ),
                    air.Div(class_='search-results-modal'),
                    class_='modal-content',
                ),
                class_='modal overflow-auto',
                id_='search-modal',
                style='display:none;',
            ),
            air.Div(hx_trigger="keyup[key=='/'] from:body"),
        air.Script("document.body.addEventListener('keydown', e => {\n            if (e.key === '/') {\n                e.preventDefault();\n
document.getElementById('search-modal').style.display = 'block';\n                document.getElementById('search-input').focus();\n
}\n            if (e.key === 'Escape') {\n                document.getElementById('search-modal').style.display = 'none';\n            }\n
});\n\n            document.getElementById('search-input').addEventListener('input', e => {\n            htmx.trigger('.search-results',
'htmx:trigger', {value: e.target.value});\n            });"),
        hx_boost='true',
        ),
    )
    """
)
