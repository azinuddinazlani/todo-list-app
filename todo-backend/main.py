from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        cursor_factory=RealDictCursor
    )
    return conn

# Pydantic model for tasks
class Task(BaseModel):
    task: str
    done: bool = False

# Create table if it doesn't exist
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

# Initialize database on startup
init_db()

# Get all tasks
@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return tasks

# Add a new task
@app.post("/tasks")
def add_task(task: Task):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task, done) VALUES (%s, %s) RETURNING *", (task.task, task.done))
    new_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_task

# Mark a task as done
@app.put("/tasks/{task_id}")
def mark_task_done(task_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = TRUE WHERE id = %s RETURNING *", (task_id,))
    updated_task = cur.fetchone()
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    conn.commit()
    cur.close()
    conn.close()
    return updated_task

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s RETURNING *", (task_id,))
    deleted_task = cur.fetchone()
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Task deleted", "task": deleted_task}