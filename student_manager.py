"""
student_manager.py

Implements student management core functionality (CRUD: Create, Read, Update, Delete)
using the OOP Student class model. Manages analytical reports and class statistics.
"""

from typing import Dict, Any, Tuple, Set, List
from .student import Student


def calculate_average(grades: Dict[str, float]) -> float:
    """
    Calculates the average score from a dictionary of subject grades.
    Handles potential division by zero when a student has no grades.
    
    Parameters:
        grades (Dict[str, float]): A mapping of subject name to score.
        
    Returns:
        float: The calculated average, or 0.0 if there are no grades.
    """
    if not grades:
        return 0.0
    total = sum(grades.values())
    return round(total / len(grades), 2)


def convert_to_gpa(average: float) -> Tuple[float, str]:
    """
    Maps a numeric average score (0-100) to a standard 4.0 scale GPA and letter grade.
    
    Parameters:
        average (float): The average grade out of 100.
        
    Returns:
        Tuple[float, str]: A tuple containing the (GPA value, Letter Grade).
    """
    if average >= 90.0:
        return 4.0, "A"
    elif average >= 80.0:
        return 3.0, "B"
    elif average >= 70.0:
        return 2.0, "C"
    elif average >= 60.0:
        return 1.0, "D"
    else:
        return 0.0, "F"


def add_student(db: Dict[str, Student], email: str, name: str, age: int, course: str, completed_modules: List[str] = None) -> Tuple[bool, str]:
    """
    Adds a new Student object to the database dictionary.
    Ensures that student emails (primary keys) are unique.
    
    Parameters:
        db (Dict[str, Student]): The in-memory student database.
        email (str): Unique email address of the student.
        name (str): Full name of the student.
        age (int): Student age.
        course (str): Course name.
        completed_modules (List[str], optional): Completed modules list.
        
    Returns:
        Tuple[bool, str]: Success status (True/False) and a descriptive message.
    """
    email = email.strip().lower()
    if email in db:
        return False, f"A student with email '{email}' already exists in the system."
        
    db[email] = Student(
        name=name,
        email=email,
        course=course,
        completed_modules=completed_modules,
        age=age,
        status="Active"
    )
    return True, f"Student '{name}' added successfully with Email: {email}."


def update_student(db: Dict[str, Student], email: str, 
                   name: str = None, 
                   age: int = None, 
                   course: str = None,
                   completed_modules: List[str] = None,
                   status: str = None) -> Tuple[bool, str]:
    """
    Updates mutable fields of a Student object.
    
    Parameters:
        db (Dict[str, Student]): The student database.
        email (str): Email of the student to update.
        name (str, optional): New name.
        age (int, optional): New age.
        course (str, optional): New course name.
        completed_modules (List[str], optional): New list of completed modules.
        status (str, optional): New enrollment status.
        
    Returns:
        Tuple[bool, str]: Success status (True/False) and a descriptive message.
    """
    email = email.strip().lower()
    if email not in db:
        return False, f"Student with email '{email}' not found."
        
    student = db[email]
    if name is not None:
        student.name = name.strip()
    if age is not None:
        student.age = age
    if course is not None:
        student.course = course.strip()
    if completed_modules is not None:
        student.completed_modules = completed_modules
    if status is not None:
        student.status = status.strip()
        
    return True, f"Student details for '{email}' updated successfully."


def add_or_update_grade(db: Dict[str, Student], email: str, subject: str, grade: float) -> Tuple[bool, str]:
    """
    Records or updates a grade for a subject in a student's record.
    
    Parameters:
        db (Dict[str, Student]): The student database.
        email (str): Student email.
        subject (str): The subject name.
        grade (float): Score (0.0 to 100.0).
        
    Returns:
        Tuple[bool, str]: Success status (True/False) and message.
    """
    email = email.strip().lower()
    if email not in db:
        return False, f"Student with email '{email}' not found."
        
    db[email].grades[subject.strip()] = grade
    return True, f"Grade {grade} for subject '{subject}' updated for Student: {email}."


def add_completed_module(db: Dict[str, Student], email: str, module_name: str) -> Tuple[bool, str]:
    """
    Appends a completed module to a student's list of modules.
    
    Parameters:
        db (Dict[str, Student]): The student database.
        email (str): Student email.
        module_name (str): Name of the completed module.
        
    Returns:
        Tuple[bool, str]: Success status (True/False) and message.
    """
    email = email.strip().lower()
    if email not in db:
        return False, f"Student with email '{email}' not found."
        
    db[email].add_module(module_name)
    return True, f"Module '{module_name}' added for Student: {email}."


def delete_student(db: Dict[str, Student], email: str) -> Tuple[bool, str]:
    """
    Removes a student record from the database.
    
    Parameters:
        db (Dict[str, Student]): The student database.
        email (str): Email of the student to delete.
        
    Returns:
        Tuple[bool, str]: Success status (True/False) and message.
    """
    email = email.strip().lower()
    if email not in db:
        return False, f"Student with email '{email}' not found."
        
    deleted_name = db[email].name
    del db[email]
    return True, f"Student '{deleted_name}' ({email}) has been removed from records."


def search_students(db: Dict[str, Student], query: str) -> Dict[str, Student]:
    """
    Searches student records. Looks for case-insensitive matches in Email,
    Name, Course, Status, or Completed Module names.
    
    Parameters:
        db (Dict[str, Student]): The student database.
        query (str): Search term.
        
    Returns:
        Dict[str, Student]: A filtered database dictionary containing matches.
    """
    query = query.strip().lower()
    matches = {}
    
    for email, student in db.items():
        email_match = query in email
        name_match = query in student.name.lower()
        course_match = query in student.course.lower()
        status_match = query in student.status.lower()
        module_match = any(query in m.lower() for m in student.completed_modules)
        
        if email_match or name_match or course_match or status_match or module_match:
            matches[email] = student
            
    return matches


def generate_class_statistics(db: Dict[str, Student]) -> Dict[str, Any]:
    """
    Generates class-wide analytical metrics.
    
    Parameters:
        db (Dict[str, Student]): The student database.
        
    Returns:
        Dict[str, Any]: Analytical summary metrics.
    """
    if not db:
        return {
            "total_students": 0,
            "class_average": 0.0,
            "top_performer": None,
            "status_counts": {},
            "subject_averages": {},
            "eligible_for_cert_count": 0
        }
        
    total_students = len(db)
    student_averages = []
    top_avg = -1.0
    top_performer = None
    eligible_count = 0
    
    status_counts = {}
    subject_scores = {}
    
    for email, student in db.items():
        # Track status counts
        status_counts[student.status] = status_counts.get(student.status, 0) + 1
        
        # Track certificate eligibility
        if student.is_eligible_for_certificate():
            eligible_count += 1
            
        # Calculate grade average
        avg = calculate_average(student.grades)
        if student.grades:
            student_averages.append(avg)
            if avg > top_avg:
                top_avg = avg
                top_performer = {
                    "email": email,
                    "name": student.name,
                    "average": avg
                }
                
        # Subject-wise marks aggregation
        for subj, mark in student.grades.items():
            if subj not in subject_scores:
                subject_scores[subj] = []
            subject_scores[subj].append(mark)
            
    class_average = round(sum(student_averages) / len(student_averages), 2) if student_averages else 0.0
    
    subject_averages = {}
    for subj, marks in subject_scores.items():
        subject_averages[subj] = round(sum(marks) / len(marks), 2)
        
    return {
        "total_students": total_students,
        "class_average": class_average,
        "top_performer": top_performer,
        "status_counts": status_counts,
        "subject_averages": subject_averages,
        "eligible_for_cert_count": eligible_count
    }
