"""
main.py

The main CLI Orchestrator. Renders menus, formatted tables, gathers user inputs,
manages sub-menus, and coordinates CRUD / analytics. Automatically saves changes
to the JSON database to prevent data loss.
"""

import sys
from .utils import (
    clear_screen,
    print_banner,
    style_text,
    get_str_input,
    get_int_input,
    get_float_input,
    confirm_action,
    COLOR_GREEN,
    COLOR_YELLOW,
    COLOR_RED,
    COLOR_CYAN,
    COLOR_BLUE,
    COLOR_HEADER,
    STYLE_BOLD,
    STYLE_UNDERLINE
)
from .file_handler import load_database, save_database, export_report
from .student_manager import (
    add_student,
    update_student,
    add_or_update_grade,
    add_completed_module,
    delete_student,
    search_students,
    calculate_average,
    convert_to_gpa,
    generate_class_statistics
)
from .student import Student

DATABASE_FILE = "students_db.json"


def get_validated_email(prompt: str) -> str:
    """
    Helper loop to prompt for and validate a basic email format.
    
    Parameters:
        prompt (str): The input prompt.
        
    Returns:
        str: Validated email string.
    """
    while True:
        email = get_str_input(prompt).strip().lower()
        if "@" in email and "." in email and len(email) >= 5:
            return email
        print(style_text("Error: Invalid email format. Must contain '@' and a domain (e.g. name@domain.com).", COLOR_RED))


def display_students_table(db: dict, title: str = "Student Directory") -> None:
    """
    Renders student records in a beautifully aligned CLI table.
    Displays completed modules count and certificate eligibility status.
    
    Parameters:
        db (dict): The dictionary of student records to display.
        title (str): Header title for the table.
    """
    print_banner(title)
    if not db:
        print(style_text("No student records found to display.", COLOR_YELLOW))
        return
        
    # Table header definition
    headers = f"| {'Student Name':<16} | {'Email Address':<28} | {'Age':<3} | {'Avg %':<6} | {'GPA':<4} | {'Modules':<7} | {'Cert':<4} | {'Status':<10} |"
    divider = "-" * len(headers)
    
    print(style_text(divider, COLOR_CYAN))
    print(style_text(headers, COLOR_CYAN, STYLE_BOLD))
    print(style_text(divider, COLOR_CYAN))
    
    for email, student in sorted(db.items()):
        name = student.name
        age = student.age
        grades = student.grades
        modules_count = len(student.completed_modules)
        status = student.status
        
        # Calculate stats
        avg = calculate_average(grades)
        gpa, letter = convert_to_gpa(avg)
        
        # Certificate eligibility
        cert_status = "Yes" if student.is_eligible_for_certificate() else "No"
        cert_styled = style_text(cert_status, COLOR_GREEN if cert_status == "Yes" else COLOR_YELLOW)
        
        # Status coloring
        status_colored = status
        if status == "Active":
            status_colored = style_text(status, COLOR_GREEN)
        elif status == "Probation":
            status_colored = style_text(status, COLOR_YELLOW)
        elif status == "Graduated":
            status_colored = style_text(status, COLOR_BLUE)
            
        email_trimmed = email
        if len(email_trimmed) > 28:
            email_trimmed = email_trimmed[:25] + "..."
            
        row = f"| {name:<16} | {email_trimmed:<28} | {age:<3} | {avg:<6.1f} | {gpa:<4.1f} | {modules_count:^7} | {cert_styled:<13} | {status_colored:<19} |"
        print(row)
        
    print(style_text(divider, COLOR_CYAN))
    print(style_text(f"Total Records: {len(db)}", STYLE_BOLD))


def cli_add_student(db: dict) -> None:
    """CLI prompt wrapper to gather details and insert a new student record."""
    print_banner("Add New Student Record")
    
    email = get_validated_email("Enter Student Email: ")
    if email in db:
        print(style_text(f"Error: A student with email '{email}' already exists.", COLOR_RED))
        return
        
    name = get_str_input("Enter Student Full Name: ")
    age = get_int_input("Enter Student Age: ", min_val=1, max_val=120)
    course = get_str_input("Enter Enrolled Course Name (e.g. Python Programming): ")
    
    print("\nEnter initial completed modules separated by commas (leave empty if none):")
    modules_raw = get_str_input("Completed Modules: ", allow_empty=True)
    completed_modules = []
    if modules_raw:
        completed_modules = [m.strip() for m in modules_raw.split(",") if m.strip()]
        
    success, msg = add_student(db, email, name, age, course, completed_modules)
    if success:
        print(style_text(msg, COLOR_GREEN))
        save_database(db, DATABASE_FILE)
    else:
        print(style_text(msg, COLOR_RED))


def cli_search_students(db: dict) -> None:
    """CLI prompt wrapper to search database by Email, Name, Course, or Module."""
    print_banner("Search Student Directory")
    query = get_str_input("Enter search query (Email, Name, Course, or Module): ")
    results = search_students(db, query)
    display_students_table(results, f"Search Results for '{query}'")


def cli_manage_student_submenu(db: dict) -> None:
    """Sub-menu to manage specific details of a single student (grades, modules, profile, status)."""
    print_banner("Manage Individual Student")
    email = get_validated_email("Enter Student Email to manage: ")
    
    if email not in db:
        print(style_text(f"Error: Student with email '{email}' not found.", COLOR_RED))
        return
        
    while True:
        student = db[email]
        print(style_text(f"\nManaging Student: {student.name} ({email})", STYLE_BOLD, COLOR_BLUE))
        print(f"Course: {student.course} | Completed Modules: {len(student.completed_modules)}/16")
        print("1. Update Profile (Name, Age, Course)")
        print("2. Manage Module Completions (Add Module)")
        print("3. Record or Update Subject Grades")
        print("4. Edit Enrollment Status")
        print("5. Back to Main Menu")
        
        choice = get_int_input("\nSelect an option (1-5): ", min_val=1, max_val=5)
        
        if choice == 1:
            print(f"Current Name: {student.name}")
            new_name = get_str_input("Enter new name (leave empty to keep current): ", allow_empty=True)
            name_val = new_name if new_name else student.name
            
            print(f"Current Age: {student.age}")
            new_age_str = input("Enter new age (leave empty to keep current): ").strip()
            age_val = int(new_age_str) if new_age_str.isdigit() else student.age
            
            print(f"Current Course: {student.course}")
            new_course = get_str_input("Enter new course name (leave empty to keep current): ", allow_empty=True)
            course_val = new_course if new_course else student.course
            
            success, msg = update_student(db, email, name=name_val, age=age_val, course=course_val)
            print(style_text(msg, COLOR_GREEN))
            save_database(db, DATABASE_FILE)
            
        elif choice == 2:
            print(f"\nCompleted Modules ({len(student.completed_modules)}):")
            if student.completed_modules:
                for idx, m in enumerate(sorted(student.completed_modules), 1):
                    print(f"  {idx}. {m}")
            else:
                print("  (No modules completed yet)")
                
            print("\n1. Add Completed Module")
            print("2. Clear All Completed Modules")
            print("3. Back")
            module_choice = get_int_input("Select option (1-3): ", min_val=1, max_val=3)
            
            if module_choice == 1:
                module_name = get_str_input("Enter name of completed module: ").strip()
                if module_name:
                    success, msg = add_completed_module(db, email, module_name)
                    print(style_text(msg, COLOR_GREEN))
                    student.show_progress() # Prints progress to CLI
                    save_database(db, DATABASE_FILE)
            elif module_choice == 2:
                if confirm_action("Are you sure you want to clear all completed modules?"):
                    update_student(db, email, completed_modules=[])
                    print(style_text("Cleared all completed modules.", COLOR_GREEN))
                    save_database(db, DATABASE_FILE)
            
        elif choice == 3:
            print("\nCurrent Subject Grades:")
            if student.grades:
                for subj, score in student.grades.items():
                    print(f"  - {subj}: {score}%")
            else:
                print("  (No grades recorded yet)")
                
            subject = get_str_input("\nEnter Subject name: ")
            grade = get_float_input(f"Enter Grade for '{subject}' (0-100): ", min_val=0.0, max_val=100.0)
            
            success, msg = add_or_update_grade(db, email, subject, grade)
            print(style_text(msg, COLOR_GREEN))
            save_database(db, DATABASE_FILE)
            
        elif choice == 4:
            print(f"Current Status: {student.status}")
            print("Available statuses: 1. Active  2. Probation  3. Graduated")
            status_choice = get_int_input("Select new status (1-3): ", min_val=1, max_val=3)
            status_map = {1: "Active", 2: "Probation", 3: "Graduated"}
            
            update_student(db, email, status=status_map[status_choice])
            print(style_text(f"Status updated to '{status_map[status_choice]}'.", COLOR_GREEN))
            save_database(db, DATABASE_FILE)
            
        elif choice == 5:
            break


def cli_delete_student(db: dict) -> None:
    """CLI prompt wrapper to safely remove a student with confirmation prompt."""
    print_banner("Delete Student Record")
    email = get_validated_email("Enter Student Email to delete: ")
    
    if email not in db:
        print(style_text(f"Error: Student with email '{email}' not found.", COLOR_RED))
        return
        
    student_name = db[email].name
    confirmed = confirm_action(f"Are you sure you want to permanently delete student {student_name} ({email})?")
    
    if confirmed:
        success, msg = delete_student(db, email)
        print(style_text(msg, COLOR_GREEN))
        save_database(db, DATABASE_FILE)
    else:
        print(style_text("Delete operation cancelled.", COLOR_YELLOW))


def cli_display_statistics(db: dict) -> None:
    """Calculates and renders class statistics report."""
    print_banner("Class Analytics & Insights")
    stats = generate_class_statistics(db)
    
    if stats["total_students"] == 0:
        print(style_text("No class statistics available. Database is empty.", COLOR_YELLOW))
        return
        
    print(f"Total Enrolled Students       : {stats['total_students']}")
    print(f"Class Grade Average           : {stats['class_average']}%")
    print(f"Eligible for Cert (16 Modules): {stats['eligible_for_cert_count']} student(s)")
    
    top = stats["top_performer"]
    if top:
        print(f"Top Performer                 : {top['name']} ({top['email']}) with Average of {top['average']}%")
    else:
        print("Top Performer                 : N/A (No grades registered)")
        
    print("\nEnrollment Status Distribution:")
    for status, count in stats["status_counts"].items():
        print(f"  - {status:<10}: {count} student(s)")
        
    print("\nCourse Subject-wise Grade Averages:")
    if stats["subject_averages"]:
        for subj, avg in sorted(stats["subject_averages"].items()):
            print(f"  - {subj:<20}: {avg}%")
    else:
        print("  (No subject averages available)")


def cli_export_report(db: dict) -> None:
    """Exports a formatted class-wide grade and analytics report to a text file."""
    print_banner("Export Class Grade Report")
    stats = generate_class_statistics(db)
    
    if stats["total_students"] == 0:
        print(style_text("Nothing to export. Database is empty.", COLOR_YELLOW))
        return
        
    # Constructing a structured report text
    report = []
    report.append("=" * 60)
    report.append("PYTHON STUDENT RECORD SYSTEM - CLASS REPORT CARD")
    report.append("=" * 60)
    report.append(f"Total Students: {stats['total_students']}")
    report.append(f"Class Average : {stats['class_average']}%")
    report.append(f"Cert Eligible : {stats['eligible_for_cert_count']} student(s)")
    
    top = stats["top_performer"]
    if top:
        report.append(f"Top Performer : {top['name']} ({top['email']}) - {top['average']}%")
    else:
        report.append("Top Performer : N/A")
        
    report.append("\n" + "-" * 40)
    report.append("Enrollment Status Summary:")
    for stat, count in stats["status_counts"].items():
        report.append(f"  {stat:<12}: {count}")
        
    report.append("\n" + "-" * 40)
    report.append("Subject-wise Performance:")
    for subj, avg in sorted(stats["subject_averages"].items()):
        report.append(f"  {subj:<25}: {avg}%")
        
    report.append("\n" + "=" * 60)
    report.append("INDIVIDUAL GRADE DIRECTORY")
    report.append("=" * 60)
    
    for email, student in sorted(db.items()):
        avg = calculate_average(student.grades)
        gpa, letter = convert_to_gpa(avg)
        progress_pct = (len(student.completed_modules) / 16) * 100
        if progress_pct > 100.0:
            progress_pct = 100.0
            
        report.append(f"\nStudent Name: {student.name}")
        report.append(f"Email Address: {email} (Age: {student.age})")
        report.append(f"Course       : {student.course}")
        report.append(f"Status       : {student.status}")
        report.append(f"Modules Done : {len(student.completed_modules)}/16 ({progress_pct:.1f}% completed)")
        report.append(f"Cert Eligible: {'Yes' if student.is_eligible_for_certificate() else 'No'}")
        report.append(f"Average Grade: {avg}% (GPA: {gpa} | Letter Grade: {letter})")
        report.append("Grades       :")
        if student.grades:
            for sub, score in student.grades.items():
                report.append(f"  * {sub}: {score}%")
        else:
            report.append("  * (No grades recorded)")
            
    report.append("\n" + "=" * 60)
    report.append("Report End.")
    
    report_text = "\n".join(report)
    
    filename = get_str_input("Enter destination filename (e.g. class_report.txt): ")
    if not filename.endswith(".txt"):
        filename += ".txt"
        
    export_report(report_text, filename)


def run_app() -> None:
    """The main loop orchestrator of the CLI application."""
    clear_screen()
    db = load_database(DATABASE_FILE)
    
    while True:
        print_banner("🎓 Python Student Record System (Module 1 Capstone)")
        print("1. View Student Directory")
        print("2. Add New Student")
        print("3. Search Student Records")
        print("4. Manage Individual Student (Grades, Profile, Modules)")
        print("5. Delete Student Record")
        print("6. View Class Analytics & Stats")
        print("7. Export Class Grade Report")
        print("8. Save & Exit Program")
        
        try:
            choice = get_int_input("\nSelect an Option (1-8): ", min_val=1, max_val=8)
            
            if choice == 1:
                display_students_table(db)
            elif choice == 2:
                cli_add_student(db)
            elif choice == 3:
                cli_search_students(db)
            elif choice == 4:
                cli_manage_student_submenu(db)
            elif choice == 5:
                cli_delete_student(db)
            elif choice == 6:
                cli_display_statistics(db)
            elif choice == 7:
                cli_export_report(db)
            elif choice == 8:
                save_database(db, DATABASE_FILE)
                print(style_text("\nDatabase saved successfully. Goodbye!", COLOR_GREEN))
                break
                
            input(style_text("\nPress Enter to return to the Main Menu...", COLOR_CYAN))
            clear_screen()
            
        except (KeyboardInterrupt, EOFError):
            print(style_text("\nSaving data changes and exiting gracefully...", COLOR_YELLOW))
            save_database(db, DATABASE_FILE)
            print(style_text("System shut down successfully. Goodbye!", COLOR_GREEN))
            sys.exit(0)


if __name__ == "__main__":
    run_app()
