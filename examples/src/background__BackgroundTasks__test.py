from pathlib import Path

from fastapi.testclient import TestClient

from .background__BackgroundTasks import app

client = TestClient(app)


def test_send_notification():
    log_file = Path("log.txt")
    if log_file.exists():
        log_file.unlink()

    response = client.post("/send-notification/john@example.com")

    assert response.status_code == 200
    assert "Notification sent to john@example.com" in response.text

    assert log_file.exists()
    log_content = log_file.read_text()
    assert "notification for john@example.com: some notification" in log_content

    log_file.unlink()
