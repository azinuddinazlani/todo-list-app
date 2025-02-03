import sys
import os
from fastapi.testclient import TestClient  # Add this import

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_task():
    response = client.post(
        "/tasks",
        json={"task": "Test task", "done": False}
    )
    assert response.status_code == 200
    assert response.json()["task"] == "Test task"

def test_mark_task_done():
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

def test_delete_task():
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