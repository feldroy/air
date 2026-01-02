# Background Tasks

Background Tasks are Python functions that are called after a response is returned to the user. They are useful for long running tasks like emails or batch processing.

Background tasks in Air, for those times a long-running process is needed that doesn't force the user to wait.

## BackgroundTasks

Bases: `BackgroundTasks`

A collection of background tasks that will be called after a response has been sent to the client.

Example:

```
import pathlib

import air

app = air.Air()


def write_notification(email: str, message: str = "") -> None:
    content = f"notification for {email}: {message}"
    pathlib.Path("log.txt").write_text(content)


@app.post("/send-notification/{email}")
def send_notification(email: str, background_tasks: air.BackgroundTasks) -> air.P:
    message = "some notification"
    background_tasks.add_task(write_notification, email, message=message)
    return air.P(f"Notification sent to {email}")
```

### add_task

```
add_task(func, *args, **kwargs)
```

Add a function to be called in the background after the response is sent.

Source code in `src/air/background.py`

```
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
```
