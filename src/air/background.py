from fastapi.background import BackgroundTasks as FastAPIBackgroundTasks
from typing_extensions import Annotated, Any, Callable, Doc, ParamSpec

P = ParamSpec("P")


class BackgroundTasks(FastAPIBackgroundTasks):
    """
    A collection of background tasks that will be called after a response has been
    sent to the client.

    ## Example

    ```python
    from air import BackgroundTasks, Air
    from air.layouts import picocss

    app = Air()


    def write_notification(email: str, message=""):
        with open("log.txt", mode="w") as email_file:
            content = f"notification for {email}: {message}"
            email_file.write(content)


    @app.post("/send-notification/{email}")
    async def send_notification(email: str, background_tasks: BackgroundTasks):
        message = "some notification"
        background_tasks.add_task(write_notification, email, message=message)
        content = f"notification for {email}: {message}"
        return picocss(
            air.Title(content),
            air.H1(content)
        )
    ```
    """

    def add_task(
        self,
        func: Annotated[
            Callable[P, Any],
            Doc(
                """
                The function to call after the response is sent.

                It can be a regular `def` function or an `async def` function.
                """
            ),
        ],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        """
        Add a function to be called in the background after the response is sent.
        """
        return super().add_task(func, *args, **kwargs)
