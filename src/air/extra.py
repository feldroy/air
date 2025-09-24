from types import ModuleType
from typing import TYPE_CHECKING
import sys

# TODO -> Do the import just when you are calling:
#         from air import auth
#         from air.auth import Something
#         from air import db
#         from air.db import Something

try:
    import auth as auth  # provided by extra: air[auth]
except ModuleNotFoundError as exc:
    msg = "Extra feature 'auth' is not installed. Install with: `uv add air[auth]`"
    raise ModuleNotFoundError(msg) from exc
else:
    # allow: from air.auth import Something
    sys.modules.setdefault(f"{__name__}.auth", auth)

try:
    import db as db  # provided by extra: air[db]
except ModuleNotFoundError as exc:
    msg = "Extra feature 'db' is not installed. Install with: `uv add air[db]`"
    raise ModuleNotFoundError(msg) from exc
else:
    # allow: from air.db import Something
    sys.modules.setdefault(f"{__name__}.db", db)

if TYPE_CHECKING:
    # Static typing: these names exist for type checkers.
    import auth as auth
    import db as db
