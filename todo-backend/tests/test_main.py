import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from main import get_db_connection, init_db

@pytest.fixture(scope="module")
def test_db():
    # Setup: Initialize the database and create tables
    init_db()
    conn = get_db_connection()
    cur = conn.cursor()

    yield conn  # Provide the database connection to the tests

    # Teardown: Clean up the database after tests
    cur.execute("DELETE FROM tasks")  # Clear the tasks table
    conn.commit()
    cur.close()
    conn.close()

@pytest.fixture
def client(test_db):
    # Use the test database connection for the client
    app.dependency_overrides[get_db_connection] = lambda: test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}  # Reset overrides after the test

def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_task(client):
    response = client.post(
        "/tasks",
        json={"task": "Test task", "done": False}
    )
    assert response.status_code == 200
    assert response.json()["task"] == "Test task"

def test_add_task_invalid_input(client):
    response = client.post(
        "/tasks",
        json={"task": "", "done": False}
    )
    assert response.status_code == 422  # Unprocessable Entity

def test_mark_task_done(client):
    # First, add a task
    response = client.post(
        "/tasks",
        json={"task": "Test task", "done": False}
    )
    task_id = response.json()["id"]

    # Mark the task as done
    response = client.put(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["done"] == True

def test_delete_task(client):
    # First, add a task
    response = client.post(
        "/tasks",
        json={"task": "Test task", "done": False}
    )
    task_id = response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted"

def test_mark_task_done_nonexistent_task(client):
    response = client.put("/tasks/9999")  # Non-existent task ID
    assert response.status_code == 404

def test_delete_task_nonexistent_task(client):
    response = client.delete("/tasks/9999")  # Non-existent task ID
    assert response.status_code == 404
