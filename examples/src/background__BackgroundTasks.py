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
