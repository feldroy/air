"""Background tasks in Air, for those times a long-running process is needed that doesn't force the user to wait."""

from collections.abc import Callable
from typing import Annotated

from fastapi.background import BackgroundTasks as FastAPIBackgroundTasks
from typing_extensions import Doc


class BackgroundTasks(FastAPIBackgroundTasks):
    """A collection of background tasks that will be called after a response has been
    sent to the client.

    Example:

        import air

        app = air.Air()


        def write_notification(email: str, message=""):
            with open("log.txt", mode="w") as email_file:
                content = f"notification for {email}: {message}"
                email_file.write(content)


        @app.post("/send-notification/{email}")
        def send_notification(email: str, background_tasks: air.BackgroundTasks):
            message = "some notification"
            background_tasks.add_task(write_notification, email, message=message)
            return air.P(f"Notification sent to {email}")


        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="0.0.0.0", port=8000)
    """

    def add_task[**P, T](
        self,
        func: Annotated[
            Callable[P, T],
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
        """Add a function to be called in the background after the response is sent."""
        return super().add_task(func, *args, **kwargs)
