"""A FastAPI-powered breath of fresh air in Python web development."""

__version__ = "0.12.0"

from . import layouts as layouts
from . import svg as svg
from .applications import Air as Air
from .forms import AirForm as AirForm
from .requests import is_htmx_request as is_htmx_request
from .responses import AirResponse as AirResponse
from .responses import TagResponse as TagResponse
from .tags import (
    H1 as H1,
)
from .tags import (
    H2 as H2,
)
from .tags import (
    H3 as H3,
)
from .tags import (
    H4 as H4,
)
from .tags import (
    H5 as H5,
)
from .tags import (
    H6 as H6,
)
from .tags import (
    A as A,
)
from .tags import (
    Abbr as Abbr,
)
from .tags import (
    Address as Address,
)
from .tags import (
    Area as Area,
)
from .tags import (
    Article as Article,
)
from .tags import (
    Aside as Aside,
)
from .tags import (
    Audio as Audio,
)
from .tags import (
    B as B,
)
from .tags import (
    Base as Base,
)
from .tags import (
    Bdi as Bdi,
)
from .tags import (
    Bdo as Bdo,
)
from .tags import (
    Blockquote as Blockquote,
)
from .tags import (
    Body as Body,
)
from .tags import (
    Br as Br,
)
from .tags import (
    Button as Button,
)
from .tags import (
    Canvas as Canvas,
)
from .tags import (
    Caption as Caption,
)
from .tags import (
    Cite as Cite,
)
from .tags import (
    Code as Code,
)
from .tags import (
    Col as Col,
)
from .tags import (
    Colgroup as Colgroup,
)
from .tags import (
    Data as Data,
)
from .tags import (
    Datalist as Datalist,
)
from .tags import (
    Dd as Dd,
)
from .tags import (
    Del as Del,
)
from .tags import (
    Details as Details,
)
from .tags import (
    Dfn as Dfn,
)
from .tags import (
    Dialog as Dialog,
)
from .tags import (
    Div as Div,
)
from .tags import (
    Dl as Dl,
)
from .tags import (
    Dt as Dt,
)
from .tags import (
    Em as Em,
)
from .tags import (
    Embed as Embed,
)
from .tags import (
    Fieldset as Fieldset,
)
from .tags import (
    Figcaption as Figcaption,
)
from .tags import (
    Figure as Figure,
)
from .tags import (
    Footer as Footer,
)
from .tags import (
    Form as Form,
)
from .tags import (
    Head as Head,
)
from .tags import (
    Header as Header,
)
from .tags import (
    Hgroup as Hgroup,
)
from .tags import (
    Hr as Hr,
)
from .tags import (
    Html as Html,
)
from .tags import (
    I as I,
)
from .tags import (
    Iframe as Iframe,
)
from .tags import (
    Img as Img,
)
from .tags import (
    Input as Input,
)
from .tags import (
    Ins as Ins,
)
from .tags import (
    Kbd as Kbd,
)
from .tags import (
    Label as Label,
)
from .tags import (
    Legend as Legend,
)
from .tags import (
    Li as Li,
)
from .tags import (
    Link as Link,
)
from .tags import (
    Main as Main,
)
from .tags import (
    Map as Map,
)
from .tags import (
    Mark as Mark,
)
from .tags import (
    Menu as Menu,
)
from .tags import (
    Meta as Meta,
)
from .tags import (
    Meter as Meter,
)
from .tags import (
    Nav as Nav,
)
from .tags import (
    Noscript as Noscript,
)
from .tags import (
    Object as Object,
)
from .tags import (
    Ol as Ol,
)
from .tags import (
    Optgroup as Optgroup,
)
from .tags import (
    Option as Option,
)
from .tags import (
    Output as Output,
)
from .tags import (
    P as P,
)
from .tags import (
    Param as Param,
)
from .tags import (
    Picture as Picture,
)
from .tags import (
    Pre as Pre,
)
from .tags import (
    Progress as Progress,
)
from .tags import (
    Q as Q,
)
from .tags import (
    RawHTML as RawHTML,
)
from .tags import (
    Rp as Rp,
)
from .tags import (
    Rt as Rt,
)
from .tags import (
    Ruby as Ruby,
)
from .tags import (
    S as S,
)
from .tags import (
    Samp as Samp,
)
from .tags import (
    Script as Script,
)
from .tags import (
    Search as Search,
)
from .tags import (
    Section as Section,
)
from .tags import (
    Select as Select,
)
from .tags import (
    Small as Small,
)
from .tags import (
    Source as Source,
)
from .tags import (
    Span as Span,
)
from .tags import (
    Strong as Strong,
)
from .tags import (
    Style as Style,
)
from .tags import (
    Sub as Sub,
)
from .tags import (
    Summary as Summary,
)
from .tags import (
    Sup as Sup,
)
from .tags import (
    Table as Table,
)
from .tags import Tag as Tag
from .tags import (
    Tbody as Tbody,
)
from .tags import (
    Td as Td,
)
from .tags import (
    Template as Template,
)
from .tags import (
    Textarea as Textarea,
)
from .tags import (
    Tfoot as Tfoot,
)
from .tags import (
    Th as Th,
)
from .tags import (
    Thead as Thead,
)
from .tags import (
    Time as Time,
)
from .tags import (
    Title as Title,
)
from .tags import (
    Tr as Tr,
)
from .tags import (
    Track as Track,
)
from .tags import (
    U as U,
)
from .tags import (
    Ul as Ul,
)
from .tags import (
    Var as Var,
)
from .tags import (
    Video as Video,
)
from .tags import (
    Wbr as Wbr,
)
from .tags import html_to_airtags as html_to_airtags
from .templates import Jinja2Renderer as Jinja2Renderer
