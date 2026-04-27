import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/project.db")


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assignee TEXT,
            priority TEXT,
            status TEXT,
            deadline TEXT,
            effort_points INTEGER,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_description (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meeting_minutes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcript TEXT,
            minutes TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_type TEXT,
            requirement_text TEXT,
            priority TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story TEXT,
            acceptance_criteria TEXT,
            priority TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            skill_level TEXT,
            hourly_rate REAL,
            availability TEXT,
            created_at TEXT
        )
    """)
        # Seed default lead resources (only if table is empty)
    cursor.execute("SELECT COUNT(*) FROM resources")
    count = cursor.fetchone()[0]

    if count == 0:
        default_resources = [
            # Project & Analysis
            ("Ali Khan", "Project Manager", "Lead", 90.0, "Available"),
            ("Emily Clark", "Business Analyst", "Senior", 75.0, "Available"),

            # Development Team
            ("John Smith", "Senior Software Developer", "Senior", 95.0, "Available"),
            ("Robert Wilson", "Backend Developer", "Mid", 70.0, "Available"),
            ("Sophia Martinez", "Frontend Developer", "Mid", 68.0, "Available"),
            ("David Chen", "Software Developer", "Junior", 45.0, "Available"),

            # Design
            ("Sara Ahmed", "UI/UX Designer", "Senior", 72.0, "Available"),
            ("Liam Brown", "UI/UX Designer", "Junior", 40.0, "Available"),

            # QA
            ("Aisha Noor", "QA Tester", "Mid", 60.0, "Available"),
            ("Daniel Kim", "QA Tester", "Junior", 42.0, "Available"),

            # DevOps & Security
            ("Michael Lee", "DevOps Engineer", "Senior", 88.0, "Available"),
            ("David Brown", "Security Analyst", "Senior", 85.0, "Available"),

            # Support roles
            ("Olivia Garcia", "Accountant", "Mid", 55.0, "Available"),
            ("Ethan White", "Procurement Manager", "Senior", 65.0, "Available"),
        ]

        for r in default_resources:
            cursor.execute("""
                INSERT INTO resources (name, role, skill_level, hourly_rate, availability, created_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, r)
    conn.commit()
    conn.close()


def add_task(title, description, assignee, priority, status, deadline, effort_points):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks 
        (title, description, assignee, priority, status, deadline, effort_points, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        assignee,
        priority,
        status,
        str(deadline),
        effort_points,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks ORDER BY deadline ASC")
    rows = cursor.fetchall()

    conn.close()

    return rows
def save_project_description(description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO project_description (description, created_at)
        VALUES (?, ?)
    """, (
        description,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_meeting_minutes(transcript, minutes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meeting_minutes (transcript, minutes, created_at)
        VALUES (?, ?, ?)
    """, (
        transcript,
        minutes,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_requirement(requirement_type, requirement_text, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO requirements 
        (requirement_type, requirement_text, priority, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        requirement_type,
        requirement_text,
        priority,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def save_user_story(story, acceptance_criteria, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_stories 
        (story, acceptance_criteria, priority, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        story,
        acceptance_criteria,
        priority,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_project_descriptions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM project_description ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_meeting_minutes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM meeting_minutes ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_requirements():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM requirements ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_user_stories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_stories ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()
    return rows

def get_full_project_context():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT description FROM project_description ORDER BY created_at DESC LIMIT 1")
    project_description = cursor.fetchone()

    cursor.execute("SELECT requirement_type, requirement_text, priority FROM requirements ORDER BY created_at DESC")
    requirements = cursor.fetchall()

    cursor.execute("SELECT story, acceptance_criteria, priority FROM user_stories ORDER BY created_at DESC")
    user_stories = cursor.fetchall()

    cursor.execute("SELECT minutes FROM meeting_minutes ORDER BY created_at DESC LIMIT 1")
    latest_minutes = cursor.fetchone()

    conn.close()

    return {
        "project_description": project_description[0] if project_description else "",
        "requirements": requirements,
        "user_stories": user_stories,
        "latest_minutes": latest_minutes[0] if latest_minutes else ""
    }
    
def add_resource(name, role, skill_level, hourly_rate, availability):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resources
        (name, role, skill_level, hourly_rate, availability, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        role,
        skill_level,
        hourly_rate,
        availability,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_resources():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resources ORDER BY role ASC, name ASC")
    rows = cursor.fetchall()

    conn.close()
    return rows

def update_task(task_id, title, description, assignee, priority, status, deadline, effort_points):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET title = ?, description = ?, assignee = ?, priority = ?, status = ?, deadline = ?, effort_points = ?
        WHERE id = ?
    """, (
        title,
        description,
        assignee,
        priority,
        status,
        str(deadline),
        effort_points,
        task_id
    ))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()