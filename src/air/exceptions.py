from fastapi.exceptions import HTTPException as FastAPIHTTPException
from typing_extensions import Annotated, Any, Dict, Doc, Optional


class HTTPException(FastAPIHTTPException):
    """
    An HTTP exception you can raise in your own code to show errors to the client.

    This is for client errors, invalid authentication, invalid data, etc. Not for server
    errors in your code.

    ## Example

    ```python
    from air import Air, HTTPException

    app = Air()

    @app.get("/")
    async def index():
        raise HTTPException(status_code=404, detail="Item not found")
        return air.H1("You will never reach this far")
    ```
    """

    def __init__(
        self,
        status_code: Annotated[
            int,
            Doc(
                """
                HTTP status code to send to the client.
                """
            ),
        ],
        detail: Annotated[
            Any,
            Doc(
                """
                Any data to be sent to the client in the `detail` key of the JSON
                response.
                """
            ),
        ] = None,
        headers: Annotated[
            Optional[Dict[str, str]],
            Doc(
                """
                Any headers to send to the client in the response.
                """
            ),
        ] = None,
    ) -> None:
        if headers is None:
            headers = {}
        headers["content-type"] = "text/html; charset=utf-8"
        super().__init__(status_code=status_code, detail=detail, headers=headers)
