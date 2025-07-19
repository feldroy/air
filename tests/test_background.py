from fastapi.testclient import TestClient

import air


def test_background_task_in_view():
    app = air.Air()

    elements = []

    assert len(elements) == 0

    def creeping_task():
        elements.append(1)

    @app.get("/big-process")
    async def test_big_process(background_tasks: air.BackgroundTasks):
        background_tasks.add_task(creeping_task)
        return air.H1("Hello, World!")

    client = TestClient(app)
    response = client.get("/big-process")

    assert response.status_code == 200
    assert len(elements) == 1


def test_add_background_task():
    elements = []

    assert len(elements) == 0

    def creeping_task():
        elements.append(1)

    # Instantiate the task holder and add one
    tasks = air.BackgroundTasks()
    tasks.add_task(creeping_task)

    # Run the task
    tasks.tasks[0].func()

    assert len(elements) == 1
