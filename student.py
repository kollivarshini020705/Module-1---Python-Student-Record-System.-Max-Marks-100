"""
student.py

Defines the Student class which holds student profiles and tracks their progress 
through 16 academic modules to determine certificate eligibility.
"""

from typing import List, Dict


class Student:
    """
    Represents a student enrolled in a course, tracking their progress,
    grades, age, enrollment status, and certificate eligibility.
    """
    
    def __init__(self, name: str, email: str, course: str, 
                 completed_modules: List[str] = None, 
                 grades: Dict[str, float] = None, 
                 age: int = 18, 
                 status: str = "Active") -> None:
        """
        Initializes a Student object.
        
        Parameters:
            name (str): Full name of the student.
            email (str): Email address of the student (acts as primary key in dictionary storage).
            course (str): Name of the academic course enrolled in.
            completed_modules (List[str], optional): List of modules completed (target: 16).
            grades (Dict[str, float], optional): Subject name to grade score mapping.
            age (int, optional): Age of the student. Defaults to 18.
            status (str, optional): Enrollment status (e.g. Active, Probation, Graduated). Defaults to "Active".
        """
        self.name = name.strip()
        self.email = email.strip()
        self.course = course.strip()
        self.completed_modules = completed_modules if completed_modules is not None else []
        self.grades = grades if grades is not None else {}
        self.age = age
        self.status = status.strip()

    def add_module(self, module_name: str) -> None:
        """
        Appends a module name to the list of completed modules.
        Checks for uniqueness to avoid duplicate entries.
        
        Parameters:
            module_name (str): The name of the completed module.
        """
        cleaned_module = module_name.strip()
        if cleaned_module and cleaned_module not in self.completed_modules:
            self.completed_modules.append(cleaned_module)

    def show_progress(self) -> float:
        """
        Calculates and prints the student's completion progress percentage 
        based on the target of 16 modules.
        
        Returns:
            float: The calculated completion percentage (capped at 100.0%).
        """
        total_required_modules = 16
        completed_count = len(self.completed_modules)
        
        # Calculate percentage
        percentage = (completed_count / total_required_modules) * 100
        # Cap percentage at 100% in case extra modules are added
        if percentage > 100.0:
            percentage = 100.0
            
        print(f"Student: {self.name} ({self.email}) | Progress: {completed_count}/{total_required_modules} modules ({percentage:.1f}%)")
        return round(percentage, 2)


    def is_eligible_for_certificate(self) -> bool:
        """
        Determines certificate eligibility. A student qualifies if they have completed 
        all 16 modules.
        
        Returns:
            bool: True if eligible, False otherwise.
        """
        return len(self.completed_modules) >= 16
