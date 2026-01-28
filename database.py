import sqlite3
from datetime import datetime

DATABASE_NAME = "todo_app.db"

def get_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def init_db():
    """Initialize the database with tasks table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            deadline TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            email TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def add_task(title, description, deadline, priority, email):
    """Add a new task to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO tasks (title, description, deadline, priority, email)
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, deadline, priority, email))
    
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    
    return task_id

def get_all_tasks(filter_status="All", sort_by="Deadline"):
    """Retrieve all tasks from the database with filtering and sorting"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks"
    
    # Apply filter
    if filter_status != "All":
        query += f" WHERE status = '{filter_status}'"
    
    # Apply sorting
    if sort_by == "Deadline":
        query += " ORDER BY deadline ASC"
    elif sort_by == "Priority":
        # Custom order: High, Medium, Low
        query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 END"
    elif sort_by == "Date Added":
        query += " ORDER BY created_at DESC"
    
    cursor.execute(query)
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks

def get_task_by_id(task_id):
    """Retrieve a single task by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    
    return task

def update_task_status(task_id, status):
    """Update the status of a task"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE tasks SET status = ? WHERE id = ?
    """, (status, task_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    conn.commit()
    conn.close()

def get_upcoming_tasks(days_ahead=3):
    """Get tasks with deadlines within specified days"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM tasks 
        WHERE status = 'Pending' 
        AND date(deadline) <= date('now', '+' || ? || ' days')
        ORDER BY deadline ASC
    """, (days_ahead,))
    
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks
