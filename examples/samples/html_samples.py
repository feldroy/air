from inspect import cleandoc
from typing import Final

FRAGMENT_HTML_SAMPLE: Final = cleandoc(
    """
    <div>
      <meta charset="utf-8">
      <meta content="width=device-width,initial-scale=1" name="viewport">
      <title>Title!</title>
      <!-- My crazy comment -->
      <p>Hello <strong>World</strong>!</p>
    </div>
    """
)

TINY_HTML_SAMPLE: Final = cleandoc(
    """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Title!</title>
        <!-- My crazy comment -->
      </head>
      <body>
        <p>Hello <strong>World</strong>!</p>
        <div hidden draggable="true" show="false" translate="no" contenteditable="true" tabindex="3" width="12.34">
          Div
        </div>
      </body>
    </html>
    """
)

SMALL_HTML_SAMPLE: Final = cleandoc(
    """
    <!doctype html>
    <html>
      <head></head>
      <body>
        <div id="id1" kwarg1="kwarg1" kwarg2="kwarg2" kwarg3="kwarg3" class="class1" style="style1">
          <link href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" rel="stylesheet">
          <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
          <h1 data-cloud data-earth>H1</h1>
          <h2 data-cloud data-earth>H1</h2>
          <p>
            <a data-cloud data-earth>A</a>
            <a id="id1">:root & > < { --pico-font-size: 100%; }</a>safe <> string<a id="id1">:root & > < { --pico-font-size: 100%; }</a>
            <img selected bar="foo" src="https://cdn.jsdelivr.net/dist/img.png" width="250" height="100" alt="My Img"><><script crossorigin="anonymous">safe <> Script</script>
          </p>
        </div>
      </body>
    </html>
    """
)

HTML_SAMPLE: Final = cleandoc(
    """
    <!doctype html>
    <html>
      <head>
        <meta property="og:image" content="https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg">
        <meta property="og:site_name" content="https://daniel.feldroy.com">
        <meta property="og:image:type" content="image/png">
        <meta property="og:type" content="website">
        <meta property="og:url" content="http://daniel.feldroy.com/">
        <meta property="og:title" content="Daniel Roy Greenfeld">
        <meta property="og:description" content="Daniel Roy Greenfeld's personal blog">
        <meta content="https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg" name="twitter:image">
        <meta content="summary" name="twitter:card">
        <meta content="Daniel Roy Greenfeld" name="twitter:title">
        <meta content="Daniel Roy Greenfeld's personal blog" name="twitter:description">
        <link href="http://daniel.feldroy.com/" rel="canonical">
        <link href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.6/dist/htmx.min.js" crossorigin="anonymous" integrity="sha384-Akqfrbj/HpNVo8k11SXBb6TlBWmXXlYQrCSqEWmyKJe+hDm3Z/B2WVG4smwBkRVm"></script>
        <style>:root { --pico-font-size: 100%; }</style>
        <link href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-dark.css" media="(prefers-color-scheme: dark)" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/styles/atom-one-light.css" media="(prefers-color-scheme: light)" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/python.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/javascript.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/html.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release/build/languages/css.min.js"></script>
        <link href="/public/style.css" rel="stylesheet" type="text/css">
        <title>Daniel Roy Greenfeld</title>
      </head>
      <body hx-boost="true">
        <header style="text-align: center;">
          <a href="/">
            <img src="https://f004.backblazeb2.com/file/daniel-feldroy-com/public/images/profile.jpg" width="108" alt="Daniel Roy Greenfeld" class="borderCircle">
          </a>
          <a href="/">
            <h2>Daniel Roy Greenfeld</h2>
          </a>
          <p>
            <a href="/about">About</a>|<a href="/posts">Articles (715)</a>|<a href="/books">Books</a>|<a href="/jobs">Jobs</a>|<a href="/tags">Tags</a>|<a href="/search">Search</a>
          </p>
        </header>
        <main class="container">
          <div class="grid">
            <section>
              <h1>Recent Writings</h1>
              <span>
                <h2>
                  <a href="/posts/2025-07-unpack-for-keyword-arguments">Unpack for keyword arguments</a>
                </h2>
                <p>Keyword arguments can now be more narrowly typed by using typing.Unpack and typing.TypeDict.<br>
                  <small>
                    <time>July 27, 2025 at 4:55pm</time>
                  </small>
                </p>
              </span>
              <span>
                <h2>
                  <a href="/posts/2025-07-uv-run-for-testing-python-versions">uv run for running tests on versions of Python</a>
                </h2>
                <p>Using uv run with make to replace tox or nox for testing multiple versions of Python locally.<br>
                  <small>
                    <time>July 20, 2025 at 10:08am</time>
                  </small>
                </p>
              </span>
              <span>
                <h2>
                  <a href="/posts/2025-05-farewell-to-michael-ryabushkin">Farewell to Michael Ryabushkin</a>
                </h2>
                <p>In early May of 2025 Michael Ryabushkin (aka Goodwill) passed away. He was a great friend and an even better person. I will miss him dearly.<br>
                  <small>
                    <time>May 16, 2025 at 11:22am</time>
                  </small>
                </p>
              </span>
              <span>
                <h2>
                  <a href="/posts/2025-05-flexicache">Exploring flexicache</a>
                </h2>
                <p>An exploration of using flexicache for caching in Python.<br>
                  <small>
                    <time>May 09, 2025 at 8:00am</time>
                  </small>
                </p>
              </span>
              <p>
                <a href="<function%20posts%20at%200x7fa78cb1b740>">Read all articles</a>
              </p>
            </section>
            <section>
              <h1>TIL<small>(Today I learned)</small>
              </h1>
              <span>
                <h3>
                  <a href="/posts/til-2025-09-setting-environment-variables-for-pytest">Setting environment variables for pytest</a>
                </h3>
                <p>
                  <small>
                    <time>September 02, 2025 at 2:29am</time>
                  </small>
                </p>
              </span>
              <span>
                <h3>
                  <a href="/posts/til-2025-08-using-sqlmodel-asynchronously-with-fastapi-and-air-with-postgresql">Using SQLModel Asynchronously with FastAPI (and Air) with PostgreSQL</a>
                </h3>
                <p>
                  <small>
                    <time>August 29, 2025 at 5:54am</time>
                  </small>
                </p>
              </span>
              <span>
                <h3>
                  <a href="/posts/til-2025-08-single-source-version-package-builds-with-uv-redux">Single source version package builds with uv (redux)</a>
                </h3>
                <p>
                  <small>
                    <time>August 22, 2025 at 2:20am</time>
                  </small>
                </p>
              </span>
              <span>
                <h3>
                  <a href="/posts/til-2025-07-how-to-type-args-and-kwargs">How to type args and kwargs</a>
                </h3>
                <p>
                  <small>
                    <time>July 26, 2025 at 9:15am</time>
                  </small>
                </p>
              </span>
              <span>
                <h3>
                  <a href="/posts/til-2025-07-single-source-version-package-builds-with-uv">Single source version package builds with uv</a>
                </h3>
                <p>
                  <small>
                    <time>July 23, 2025 at 1:59am</time>
                  </small>
                </p>
              </span>
              <span>
                <h3>
                  <a href="/posts/til-2025-06-removing-exif-geodata-from-media">Removing exif geodata from media</a>
                </h3>
                <p>
                  <small>
                    <time>June 23, 2025 at 8:56pm</time>
                  </small>
                </p>
              </span>
              <span>
                <h3>
                  <a href="/posts/til-2025-06-html-404-errors-for-fastapi">HTML 404 errors for FastAPI</a>
                </h3>
                <p>
                  <small>
                    <time>June 13, 2025 at 4:23am</time>
                  </small>
                </p>
              </span>
              <p>
                <a href="/tags/TIL">Read more TIL articles</a>
              </p>
            </section>
            <section>
              <h1>Featured Writings</h1>
              <span>
                <h2>
                  <a href="/posts/thirty-minute-rule">The Thirty Minute Rule</a>
                </h2>
                <p>What to do when you get stuck on a coding issue for more than 30 minutes.<br>
                  <small>
                    <time>August 18, 2021 at 12:00am</time>
                  </small>
                </p>
              </span>
              <span>
                <h2>
                  <a href="/posts/whats-the-best-thing-about-working-for-octopus-energy-part-1">What's the Best Thing about Working for Octopus Energy?</a>
                </h2>
                <p>An in-depth discussion about my employment at Octopus Energy.<br>
                  <small>
                    <time>June 08, 2021 at 11:59pm</time>
                  </small>
                </p>
              </span>
              <span>
                <h2>
                  <a href="/posts/code-code-code">Code, Code, Code</a>
                </h2>
                <p>I'm often asked by new programmers how they can forge a path into using their skills professionally. Or how they can get better at writing software. In this article I share the secret master-level method to improvement.<br>
                  <small>
                    <time>May 28, 2016 at 12:00am</time>
                  </small>
                </p>
              </span>
              <span>
                <h2>
                  <a href="/posts/i-married-audrey-roy">I Married Audrey Roy</a>
                </h2>
                <p>The story of one of the best days of my life.<br>
                  <small>
                    <time>January 04, 2014 at 12:00am</time>
                  </small>
                </p>
              </span>
            </section>
          </div>
        </main>
        <footer class="container">
          <hr>
          <p>
            <a href="https://www.linkedin.com/in/danielfeldroy/" target="_blank">LinkedIn</a>|<a href="https://bsky.app/profile/daniel.feldroy.com" target="_blank">Bluesky</a>|<a href="https://twitter.com/pydanny" target="_blank">Twitter</a>|<a href="https://github.com/pydanny" target="_blank">Github</a>| Feeds:<a href="/feeds/atom.xml" target="_blank">All</a>,<a href="/feeds/python.atom.xml" target="_blank">Python</a>,<a href="/feeds/til.atom.xml" target="_blank">TIL</a>
          </p>
          <p>All rights reserved 2025, Daniel Roy Greenfeld</p>
        </footer>
        <dialog class="modal overflow-auto" id="search-modal" style="display:none;">
          <header class="modal-content">
            <h2>Search</h2>
            <input hx-trigger="keyup" hx-get="/search-results" hx-target=".search-results-modal" name="q" type="text" placeholder="Enter your search query..." id="search-input">
            <div class="search-results-modal"></div>
          </header>
        </dialog>
        <div hx-trigger="keyup from:body"></div>
        <script>document.body.addEventListener('keydown', e => {
                if (e.key === '/') {
                    e.preventDefault();
                    document.getElementById('search-modal').style.display = 'block';
                    document.getElementById('search-input').focus();
                }
                if (e.key === 'Escape') {
                    document.getElementById('search-modal').style.display = 'none';
                }
                });

                document.getElementById('search-input').addEventListener('input', e => {
                htmx.trigger('.search-results', 'htmx:trigger', {value: e.target.value});
                });</script>
      </body>
    </html>
    """
)
