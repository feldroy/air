import weakref
from urllib.parse import urlencode

from fastapi import FastAPI
from starlette.routing import BaseRoute, NoMatchFound


class UrlDescriptor:
    def __init__(self, app: FastAPI, route_name: str) -> None:
        self._app_ref = weakref.ref(app)
        self._route_name = route_name

    def __call__(self, **params):
        app = self._app_ref()
        if app is None:
            error = "Application no longer exists"
            raise RuntimeError(error)
        route: BaseRoute | None = next(
            (r for r in app.router.routes if getattr(r, "name", None) == self._route_name),
            None,
        )
        if route is None:
            raise NoMatchFound(self._route_name, {})
        path_params = set(getattr(route, "param_convertors", {}).keys())
        path_kwargs = {k: v for k, v in params.items() if k in path_params}
        query_kwargs = {k: v for k, v in params.items() if k not in path_params}
        missing = path_params - set(path_kwargs)
        if missing:
            raise NoMatchFound(self._route_name, path_kwargs)
        url = str(app.url_path_for(self._route_name, **path_kwargs))
        if query_kwargs:
            url += "?" + urlencode(query_kwargs, doseq=True)
        return url
