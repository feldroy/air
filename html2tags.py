from bs4 import BeautifulSoup, NavigableString, Comment
import subprocess


def html_to_air_tags(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    def convert_node(node):
        if isinstance(node, NavigableString):
            content = node.strip()
            return repr(content) if content else ''

        tag_name = node.name.capitalize()
        args = []

        # Convert children
        for child in node.children:
            converted = convert_node(child)
            if converted:
                args.append(converted)

        # Class attribute becomes `class_`
        if cls_value := node.get('class'):
            cls_str = ' '.join(cls_value)
            args.append(f"class_={repr(cls_str)}")

        # For attribute becomes `for_`
        if cls_value := node.get('for'):
            cls_str = ' '.join(cls_value)
            args.append(f"for_={repr(cls_str)}")        

        # Get all other attributes
        for key,value in node.attrs.items():
            if key in ['class', 'for']: continue
            if isinstance(value, list): cls_str = ' '.join(value)
            else: cls_str = value
            args.append(f"{key}={repr(cls_str)}")              


        return f"air.{tag_name}({', '.join(args)})"

    # Convert top-level tag
    source_code = convert_node(soup.body.contents[0] if soup.body else soup.contents[0])
    print(source_code)
    if source_code:
        return format_with_ruff(source_code)
    return ''


import subprocess
import tempfile
import os

def format_with_ruff(code: str) -> str:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w+", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        # Run ruff to format the file
        subprocess.run(["ruff", "format", tmp_path], check=True)

        # Read the formatted content
        with open(tmp_path, "r") as f:
            formatted_code = f.read()
    finally:
        os.remove(tmp_path)  # Clean up the temporary file

    return formatted_code



if __name__ == '__main__':
    input = """<footer class="bg-gray-800 text-white py-4">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p>&copy; 2025 Feldroy. All rights reserved.</p>
    </div>
</footer>"""
    output = """air.Footer(
    air.Div(
        air.P("© 2025 Feldroy. All rights reserved."),
        class_="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center"
    ),
    class_="bg-gray-800 text-white py-4"
)"""

    converted = html_to_air_tags(input)
    print(converted)
    assert converted == output


# @app.page
# def convert(request: air.Request):
#     title = 'Convert HTML to Air Tags'
#     return layout(
#         request,
#         air.Title(title),
#         air.H1(title),
#         air.Form(
#             air.Textarea(
#                 rows=10, cols="80",
#                 placeholder='HTML to be converted goes here...',
#                 id="html",
#                 name='html',
#                 hx_trigger="input changed delay:500ms",
#                 hx_post="/converter",
#             ),
#         ),
#         air.Hr(),
#         air.Div(
#             air.P('Nothing changed'),
#             id='result',
#             hx_swap_oob="true"
#         )
#     )


# class HtmlModel(BaseModel):
#     html: str


# class HtmlForm(air.AirForm):
#     model = HtmlModel

# @app.post('/converter')
# async def converter(request: air.Request):
#     form = await request.form()
#     html = form.get('html', '')
#     return air.Div(
#         air.Pre(
#             air.Code(html_to_air_tags(html))
#         ),
#         id='result',
#         hx_swap_oob="true",
#     )