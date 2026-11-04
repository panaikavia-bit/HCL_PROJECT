
import sqlite3
from pathlib import Path

# Database location
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "learning_progress.db"


# 30-day C# and .NET curriculum
CURRICULUM = [
    {"day": 1, "topic": "Introduction to C# and .NET",
     "tasks": ["What is C#?", "What is .NET?", "CLR, CTS and compilation"]},

    {"day": 2, "topic": "Variables and Data Types",
     "tasks": ["Variables", "int, float, string, bool", "Type conversion"]},

    {"day": 3, "topic": "Operators",
     "tasks": ["Arithmetic operators", "Comparison operators", "Logical operators"]},

    {"day": 4, "topic": "Conditional Statements",
     "tasks": ["if and else", "else-if", "switch statement"]},

    {"day": 5, "topic": "Loops",
     "tasks": ["for loop", "while loop", "do-while and foreach"]},

    {"day": 6, "topic": "Arrays",
     "tasks": ["One-dimensional arrays", "Multidimensional arrays", "Array programs"]},

    {"day": 7, "topic": "Strings",
     "tasks": ["String methods", "String manipulation", "String programs"]},

    {"day": 8, "topic": "Methods",
     "tasks": ["Method creation", "Parameters and return values", "Method overloading"]},

    {"day": 9, "topic": "Classes and Objects",
     "tasks": ["Class definition", "Creating objects", "Fields and properties"]},

    {"day": 10, "topic": "Constructors",
     "tasks": ["Default constructor", "Parameterized constructor", "Constructor overloading"]},

    {"day": 11, "topic": "Encapsulation",
     "tasks": ["Access modifiers", "Getters and setters", "Properties"]},

    {"day": 12, "topic": "Inheritance",
     "tasks": ["Base and derived classes", "Types of inheritance", "base keyword"]},

    {"day": 13, "topic": "Polymorphism",
     "tasks": ["Method overloading", "Method overriding", "Virtual and override"]},

    {"day": 14, "topic": "Abstraction and Interfaces",
     "tasks": ["Abstract classes", "Interfaces", "Abstract vs interface"]},

    {"day": 15, "topic": "Exception Handling",
     "tasks": ["try and catch", "finally", "throw keyword"]},

    {"day": 16, "topic": "Collections",
     "tasks": ["List", "Dictionary", "HashSet and Queue"]},

    {"day": 17, "topic": "Generics",
     "tasks": ["Generic classes", "Generic methods", "Type safety"]},

    {"day": 18, "topic": "LINQ",
     "tasks": ["Where", "Select", "OrderBy and GroupBy"]},

    {"day": 19, "topic": "Delegates and Events",
     "tasks": ["Delegates", "Multicast delegates", "Events"]},

    {"day": 20, "topic": "File Handling",
     "tasks": ["Read files", "Write files", "File and Stream classes"]},

    {"day": 21, "topic": "Asynchronous Programming",
     "tasks": ["async and await", "Task", "Asynchronous methods"]},

    {"day": 22, "topic": "SQL and Database Fundamentals",
     "tasks": ["Tables and keys", "SELECT and JOIN", "CRUD operations"]},

    {"day": 23, "topic": "ADO.NET",
     "tasks": ["Database connection", "SqlCommand", "DataReader"]},

    {"day": 24, "topic": "ASP.NET Core",
     "tasks": ["Introduction", "MVC basics", "Middleware"]},

    {"day": 25, "topic": "ASP.NET Core Web API",
     "tasks": ["REST API", "HTTP methods", "API controllers"]},

    {"day": 26, "topic": "OOP Revision",
     "tasks": ["Four OOP principles", "Real-world examples", "Interview questions"]},

    {"day": 27, "topic": "C# Coding Practice - I",
     "tasks": ["Reverse a string", "Palindrome", "Prime number"]},

    {"day": 28, "topic": "C# Coding Practice - II",
     "tasks": ["Array problems", "Number patterns", "Logical coding problems"]},

    {"day": 29, "topic": "Technical Mock Interview",
     "tasks": ["C# interview questions", ".NET interview questions", "Explain your answers"]},

    {"day": 30, "topic": "Final Interview Assessment",
     "tasks": ["Complete mock test", "Review weak topics", "Final revision"]}
]


# Create database table
def initialize_tracker():

    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_progress (
                day INTEGER PRIMARY KEY,
                completed INTEGER DEFAULT 0,
                minutes INTEGER DEFAULT 0,
                notes TEXT DEFAULT '',
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


# Get saved progress
def get_all_progress():

    with sqlite3.connect(DB_PATH) as conn:

        conn.row_factory = sqlite3.Row

        rows = conn.execute(
            "SELECT * FROM daily_progress"
        ).fetchall()

        return {row["day"]: dict(row) for row in rows}


# Save daily progress
def save_progress(day, completed, minutes, notes):

    with sqlite3.connect(DB_PATH) as conn:

        conn.execute("""
            INSERT INTO daily_progress
            (day, completed, minutes, notes, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)

            ON CONFLICT(day) DO UPDATE SET
                completed = excluded.completed,
                minutes = excluded.minutes,
                notes = excluded.notes,
                updated_at = CURRENT_TIMESTAMP
        """, (day, int(completed), minutes, notes))
