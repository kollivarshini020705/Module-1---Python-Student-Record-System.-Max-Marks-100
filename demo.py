"""
demo.py

A self-contained demonstration script for the Module 1 Capstone Assignment.
This script demonstrates standard Python concepts: Object-Oriented Programming (OOP)
using a Student class, dictionary storage, lists, iterations, and formatted string reports.

Minimum 50 lines of code with thorough commentary explaining each section.
"""

# =====================================================================
# SECTION 1: DEFINING THE STUDENT CLASS
# =====================================================================
class Student:
    """
    Represents a student enrolled in a course.
    Tracks module completions, progress percentages, and certificate eligibility.
    """
    
    def __init__(self, name: str, email: str, course: str, completed_modules: list = None) -> None:
        """
        Initializes a new Student object.
        """
        self.name = name
        self.email = email
        self.course = course
        # Default to empty list if no modules are passed
        self.completed_modules = completed_modules if completed_modules is not None else []

    def add_module(self, module_name: str) -> None:
        """
        Appends a module to the completed modules list, preventing duplicates.
        """
        module_name = module_name.strip()
        if module_name and module_name not in self.completed_modules:
            self.completed_modules.append(module_name)

    def show_progress(self) -> float:
        """
        Prints the progress completion percentage and returns the value.
        Based on a requirement of completing 16 modules.
        """
        total_modules = 16
        completed_count = len(self.completed_modules)
        
        # Calculate completion percentage
        percentage = (completed_count / total_modules) * 100
        # Cap percentage at 100.0%
        if percentage > 100.0:
            percentage = 100.0
            
        print(f"[ PROGRESS ] Student: {self.name} | Completed: {completed_count}/{total_modules} modules ({percentage:.1f}%)")
        return round(percentage, 2)

    def is_eligible_for_certificate(self) -> bool:
        """
        Checks if the student is eligible for a completion certificate.
        Returns True if they have completed all 16 modules, False otherwise.
        """
        return len(self.completed_modules) >= 16


# =====================================================================
# SECTION 2: CREATING STUDENT INSTANCES & INITIAL DEMONSTRATIONS
# =====================================================================
print("=" * 70)
print("DEMONSTRATING STUDENT OBJECT CREATION & METHOD WORKFLOWS")
print("=" * 70)

# Instantiate 3 student objects with different profiles and completed modules lists
student_1 = Student(
    name="Emma Watson", 
    email="emma.watson@hogwarts.edu", 
    course="Python Programming", 
    completed_modules=["Module 1", "Module 2", "Module 3", "Module 4"]
)

student_2 = Student(
    name="Daniel Radcliffe", 
    email="daniel.radcliffe@hogwarts.edu", 
    course="Web Development", 
    completed_modules=["HTML Basics", "CSS Layouts"]
)

student_3 = Student(
    name="Rupert Grint", 
    email="rupert.grint@hogwarts.edu", 
    course="Database Systems", 
    completed_modules=[]
)

print(f"Created Student 1: {student_1.name} ({student_1.email})")
print(f"Created Student 2: {student_2.name} ({student_2.email})")
print(f"Created Student 3: {student_3.name} ({student_3.email})")
print("-" * 70)


# =====================================================================
# SECTION 3: DEMONSTRATING METHOD EXECUTION
# =====================================================================

# 1. Demonstrate add_module method
print("\n--- Adding Completed Modules ---")
# Emma Watson completes her remaining modules to reach the target of 16 modules
for m in range(5, 17):
    student_1.add_module(f"Module {m}")
print(f"-> Added modules 5 through 16 to {student_1.name}. Total completed: {len(student_1.completed_modules)}")

# Daniel Radcliffe completes some additional modules
student_2.add_module("JavaScript Intro")
student_2.add_module("DOM Manipulation")
student_2.add_module("API Integrations")
print(f"-> Added 3 modules to {student_2.name}. Total completed: {len(student_2.completed_modules)}")

# Rupert Grint completes only one module
student_3.add_module("SQL Basics")
print(f"-> Added 'SQL Basics' module to {student_3.name}. Total completed: {len(student_3.completed_modules)}")

# 2. Demonstrate show_progress method (prints to console and returns percentage)
print("\n--- Displaying Progress Percentages ---")
pct_1 = student_1.show_progress()
pct_2 = student_2.show_progress()
pct_3 = student_3.show_progress()

# 3. Demonstrate is_eligible_for_certificate method
print("\n--- Verifying Certificate Eligibility ---")
for s in [student_1, student_2, student_3]:
    eligible = s.is_eligible_for_certificate()
    status_text = "ELIGIBLE" if eligible else "INELIGIBLE"
    print(f"Student: {s.name:<18} | Modules: {len(s.completed_modules):>2}/16 | Status: {status_text}")


# =====================================================================
# SECTION 4: STORE IN DICTIONARY WITH EMAIL AS KEY
# =====================================================================
# Constructing a dictionary structure mapping student email addresses to student objects
student_directory = {
    student_1.email: student_1,
    student_2.email: student_2,
    student_3.email: student_3
}


# =====================================================================
# SECTION 5: PRINTING A FORMATTED REPORT
# =====================================================================
print("\n" + "=" * 80)
print("                    ACADEMIC PROGRESS REPORT CARD                      ")
print("=" * 80)

# Formatted Table Headers
headers = f"| {'Student Name':<16} | {'Email Address':<30} | {'Completed':<9} | {'Progress':<8} | {'Cert. Eligible':<14} |"
divider = "-" * len(headers)

print(divider)
print(headers)
print(divider)

# Iterate through dictionary mapping to display student details
for email, student_obj in student_directory.items():
    completed_count = len(student_obj.completed_modules)
    progress_percent = (completed_count / 16) * 100
    if progress_percent > 100.0:
        progress_percent = 100.0
        
    eligibility_status = "Yes" if student_obj.is_eligible_for_certificate() else "No"
    
    # Render table row with column formatting specifiers
    row = f"| {student_obj.name:<16} | {email:<30} | {completed_count:>9} | {progress_percent:>7.1f}% | {eligibility_status:^14} |"
    print(row)

print(divider)
print(f"Total Enrolled Records: {len(student_directory)}")
print("=" * 80)
