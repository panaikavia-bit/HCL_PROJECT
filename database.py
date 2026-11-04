import os
import sqlite3
import json
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DATABASE_PATH", "./data/interview.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day INTEGER NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day INTEGER NOT NULL,
                question TEXT NOT NULL,
                options TEXT NOT NULL,
                answer TEXT NOT NULL,
                explanation TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_questions(day, questions):
    with get_connection() as conn:
        conn.execute("DELETE FROM questions WHERE day = ?", (day,))

        for q in questions:
            conn.execute("""
                INSERT INTO questions
                (day, question, options, answer, explanation)
                VALUES (?, ?, ?, ?, ?)
            """, (
                day,
                q["question"],
                json.dumps(q["options"]),
                q["answer"],
                q["explanation"]
            ))


def get_questions(day):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT question, options, answer, explanation
            FROM questions
            WHERE day = ?
            ORDER BY id
        """, (day,)).fetchall()

    return [
        {
            "question": row[0],
            "options": json.loads(row[1]),
            "answer": row[2],
            "explanation": row[3]
        }
        for row in rows
    ]


def save_progress(day, score, total):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO progress (day, score, total)
            VALUES (?, ?, ?)
        """, (day, score, total))


def get_progress():
    with get_connection() as conn:
        return conn.execute("""
            SELECT day, score, total, completed_at
            FROM progress
            ORDER BY completed_at DESC
        """).fetchall()


def save_chat(role, message):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO chat_history (role, message)
            VALUES (?, ?)
        """, (role, message))


def get_chat():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT role, message
            FROM chat_history
            ORDER BY id
        """).fetchall()

    return [{"role": row[0], "message": row[1]} for row in rows]


def clear_chat():
    with get_connection() as conn:
        conn.execute("DELETE FROM chat_history")