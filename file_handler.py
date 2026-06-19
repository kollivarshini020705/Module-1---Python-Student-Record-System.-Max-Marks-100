"""
file_handler.py

Handles file reading, writing, and parsing of the student database.
Integrates the OOP Student class by loading JSON data into Student instances
and serializing Student instances back to JSON.
"""

import json
import os
from typing import Dict
from .student import Student
from .utils import style_text, COLOR_YELLOW, COLOR_RED, COLOR_GREEN

# Default template database populated with realistic records for grading demonstration
# Stored with student email address as the primary dictionary key.
DEFAULT_STUDENTS = {
    "alice.johnson@example.com": {
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "course": "Python Programming",
        "completed_modules": ["Module 1", "Module 2", "Module 3", "Module 4"],
        "grades": {"Python Programming": 92.5, "Database Systems": 88.0, "Web Development": 95.0},
        "age": 20,
        "status": "Active"
    },
    "bob.smith@example.com": {
        "name": "Bob Smith",
        "email": "bob.smith@example.com",
        "course": "Web Development",
        "completed_modules": ["HTML Basics", "CSS Layouts"],
        "grades": {"Python Programming": 74.0, "Database Systems": 68.5, "Discrete Math": 71.0},
        "age": 22,
        "status": "Active"
    },
    "charlie.brown@example.com": {
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "course": "Python Programming",
        "completed_modules": ["Module 1"],
        "grades": {"Python Programming": 54.5, "Basic Writing": 62.0},
        "age": 19,
        "status": "Probation"
    },
    "diana.prince@example.com": {
        "name": "Diana Prince",
        "email": "diana.prince@example.com",
        "course": "Python Programming",
        "completed_modules": [f"Module {x}" for x in range(1, 17)],  # All 16 modules completed
        "grades": {"Python Programming": 98.0, "Web Development": 99.5, "Algorithms": 97.0},
        "age": 21,
        "status": "Graduated"
    }
}


def load_database(filepath: str) -> Dict[str, Student]:
    """
    Loads student records from a JSON file and instantiates Student class objects.
    If the file does not exist, populates it with a set of default students.
    Handles FileNotFoundError and json.JSONDecodeError exceptions.
    
    Parameters:
        filepath (str): Path to the JSON database file.
        
    Returns:
        Dict[str, Student]: Dictionary mapping email to Student object instances.
    """
    dir_name = os.path.dirname(filepath)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    if not os.path.exists(filepath):
        print(style_text(f"Database file not found. Creating a new database with sample records at: {filepath}", COLOR_YELLOW))
        # Save a temporary copy of DEFAULT_STUDENTS
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                json.dump(DEFAULT_STUDENTS, file, indent=4)
        except IOError as e:
            print(style_text(f"Failed to create starter database file: {e}", COLOR_RED))
            
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
            
        # Reconstruct Student instances
        db = {}
        for email, details in raw_data.items():
            db[email] = Student(
                name=details.get("name", "Unknown"),
                email=details.get("email", email),
                course=details.get("course", "Python Programming"),
                completed_modules=list(details.get("completed_modules", [])),
                grades={subj: float(score) for subj, score in details.get("grades", {}).items()},
                age=int(details.get("age", 18)),
                status=details.get("status", "Active")
            )
        return db
        
    except json.JSONDecodeError:
        print(style_text("Error: Database file contains corrupted JSON data. Initializing empty database.", COLOR_RED))
        return {}
    except PermissionError:
        print(style_text("Error: Permission denied when accessing the database file. Initializing empty database.", COLOR_RED))
        return {}


def save_database(db: Dict[str, Student], filepath: str) -> bool:
    """
    Saves the student records dictionary (containing Student objects) to a JSON file.
    Converts Student objects to dictionaries prior to serialization.
    Uses context managers and handles IOExceptions safely.
    
    Parameters:
        db (Dict[str, Student]): The in-memory student records.
        filepath (str): Destination path for the database file.
        
    Returns:
        bool: True if save succeeded, False otherwise.
    """
    try:
        export_data = {}
        for email, student in db.items():
            # Check if student is a Student instance or dictionary (for legacy setup safety)
            if isinstance(student, Student):
                export_data[email] = {
                    "name": student.name,
                    "email": student.email,
                    "course": student.course,
                    "completed_modules": student.completed_modules,
                    "grades": student.grades,
                    "age": student.age,
                    "status": student.status
                }
            else:
                # Fallback support
                export_data[email] = student
                
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(export_data, file, indent=4)
        return True
    except (TypeError, PermissionError, IOError) as e:
        print(style_text(f"Error saving database to file: {e}", COLOR_RED))
        return False


def export_report(report_text: str, filepath: str) -> bool:
    """
    Exports a plain-text report (e.g. grade summaries, analytics) to a file.
    
    Parameters:
        report_text (str): The string contents of the report.
        filepath (str): Target filename for the report.
        
    Returns:
        bool: True if exported successfully, False otherwise.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(report_text)
        print(style_text(f"Success: Report exported successfully to {filepath}", COLOR_GREEN))
        return True
    except IOError as e:
        print(style_text(f"Error exporting report: {e}", COLOR_RED))
        return False
