"""
test_runner.py

Automated test suite verifying Student class methods, database CRUD operations,
and statistics reports using email keys.
"""

from src.student import Student
from src.student_manager import (
    calculate_average,
    convert_to_gpa,
    add_student,
    update_student,
    add_or_update_grade,
    add_completed_module,
    delete_student,
    search_students,
    generate_class_statistics
)


def run_tests():
    print("=" * 60)
    print("RUNNING AUTOMATED UNIT TESTS FOR OOP STUDENT RECORD SYSTEM")
    print("=" * 60)
    
    passed = 0
    failed = 0

    def assert_test(name, condition):
        nonlocal passed, failed
        if condition:
            print(f"[ PASS ] {name}")
            passed += 1
        else:
            print(f"[ FAIL ] {name}")
            failed += 1

    # --- Test Case 1: Student Class Methods ---
    test_student = Student("Test Name", "test@example.com", "Python Programming", ["Module 1"])
    assert_test("Student class instantiation", test_student.name == "Test Name" and test_student.email == "test@example.com")
    
    test_student.add_module("Module 2")
    assert_test("Student.add_module - adds unique module", "Module 2" in test_student.completed_modules and len(test_student.completed_modules) == 2)
    
    test_student.add_module("Module 2")
    assert_test("Student.add_module - blocks duplicate module", len(test_student.completed_modules) == 2)

    progress = test_student.show_progress()
    # 2/16 = 12.5%
    assert_test("Student.show_progress - percentage calculation", progress == 12.5)
    assert_test("Student.is_eligible_for_certificate - under modules limit", test_student.is_eligible_for_certificate() is False)
    
    # Fill modules to make eligible
    for i in range(3, 18):
        test_student.add_module(f"Module {i}")
    assert_test("Student.is_eligible_for_certificate - meets/exceeds modules limit", test_student.is_eligible_for_certificate() is True)

    # --- Test Case 2: Average Calculation ---
    grades_empty = {}
    grades_normal = {"Math": 80.0, "Science": 90.0}
    assert_test("calculate_average - empty grades dictionary", calculate_average(grades_empty) == 0.0)
    assert_test("calculate_average - normal average math", calculate_average(grades_normal) == 85.0)

    # --- Test Case 3: GPA Letter Grade Conversion ---
    gpa_a, letter_a = convert_to_gpa(95.0)
    gpa_f, letter_f = convert_to_gpa(55.0)
    assert_test("convert_to_gpa - 95.0 (GPA 4.0, A)", gpa_a == 4.0 and letter_a == "A")
    assert_test("convert_to_gpa - 55.0 (GPA 0.0, F)", gpa_f == 0.0 and letter_f == "F")

    # --- Setup mock database ---
    mock_db = {}

    # --- Test Case 4: Add Student to DB ---
    success_add, msg_add = add_student(mock_db, "emma@hogwarts.edu", "Emma Watson", 21, "Python Programming", ["Module 1"])
    assert_test("add_student - unique student insertion", success_add is True and "emma@hogwarts.edu" in mock_db)
    assert_test("add_student - values stored as Student object", isinstance(mock_db["emma@hogwarts.edu"], Student))
    
    success_add_dup, _ = add_student(mock_db, "emma@hogwarts.edu", "Emma Watson Dup", 22, "Web Dev")
    assert_test("add_student - blocking duplicate emails", success_add_dup is False)

    # --- Test Case 5: Record Grades and Modules in DB ---
    success_grade, _ = add_or_update_grade(mock_db, "emma@hogwarts.edu", "Math", 95.0)
    assert_test("add_or_update_grade - successful grade record", success_grade is True and mock_db["emma@hogwarts.edu"].grades["Math"] == 95.0)
    
    success_mod, _ = add_completed_module(mock_db, "emma@hogwarts.edu", "Module 2")
    assert_test("add_completed_module - database update", success_mod is True and "Module 2" in mock_db["emma@hogwarts.edu"].completed_modules)

    # --- Test Case 6: Update Student Details ---
    success_update, _ = update_student(mock_db, "emma@hogwarts.edu", age=22, status="Probation")
    assert_test("update_student - age modification", mock_db["emma@hogwarts.edu"].age == 22)
    assert_test("update_student - status modification", mock_db["emma@hogwarts.edu"].status == "Probation")

    # --- Test Case 7: Search Query logic ---
    add_student(mock_db, "daniel@hogwarts.edu", "Daniel Radcliffe", 23, "Web Development", ["HTML Basics"])
    matches_name = search_students(mock_db, "Daniel")
    matches_email = search_students(mock_db, "emma@")
    matches_course = search_students(mock_db, "Web Dev")
    assert_test("search_students - name substring match", "daniel@hogwarts.edu" in matches_name)
    assert_test("search_students - email substring match", "emma@hogwarts.edu" in matches_email)
    assert_test("search_students - course substring match", "daniel@hogwarts.edu" in matches_course)

    # --- Test Case 8: Class Analytics generation ---
    # Add grades for daniel
    add_or_update_grade(mock_db, "daniel@hogwarts.edu", "Math", 85.0)
    stats = generate_class_statistics(mock_db)
    assert_test("generate_class_statistics - total enrollment count", stats["total_students"] == 2)
    assert_test("generate_class_statistics - class average math grade", stats["subject_averages"]["Math"] == 90.0)
    assert_test("generate_class_statistics - top performer detection", stats["top_performer"]["email"] == "emma@hogwarts.edu")

    # --- Test Case 9: Delete Student from DB ---
    success_del, _ = delete_student(mock_db, "emma@hogwarts.edu")
    assert_test("delete_student - successful removal", success_del is True and "emma@hogwarts.edu" not in mock_db)
    
    success_del_fail, _ = delete_student(mock_db, "emma@hogwarts.edu")
    assert_test("delete_student - delete invalid email fails", success_del_fail is False)

    # --- Final summary ---
    print("=" * 60)
    print(f"TEST RUN SUMMARY: {passed} PASSED | {failed} FAILED")
    print("=" * 60)
    
    if failed > 0:
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    run_tests()
