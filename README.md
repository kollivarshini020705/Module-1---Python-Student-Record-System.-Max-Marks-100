# 🎓 Python Student Record System

An elegant, premium Command-Line Interface (CLI) application built using core Python programming concepts from Module 1. It manages student profiles, course enrollments, subject grades, and generates class-wide analytical metrics using a custom **`Student` class** structure indexed by **email address**.

---

## 🏆 Project Features

1. **Object-Oriented Student Class**: Built with data encapsulation (stores `name`, `email`, `course`, `completed_modules`, `grades`, `age`, `status`) and functional methods:
   - `add_module(module_name)`: Registers course module completions.
   - `show_progress()`: Displays progress ratios against the 16-module goal.
   - `is_eligible_for_certificate()`: Checks if $\ge 16$ modules are completed.
2. **Self-Contained OOP Demo (`demo.py`)**: A thorough, well-commented 100+ line execution script demonstrating class instantiation, method evaluations, email dictionary key storage, and formatted report cards.
3. **Interactive Shell CLI (`run.py`)**: Premium terminal layout with colored headers, banners, and options.
4. **Robust Input Validation**: Implemented using structured `try/except` loops to prevent input types or range boundary overflows from crashing the system.
5. **Persistent JSON Database**: Auto-loads records on startup and automatically commits changes locally using standard file I/O operations.
6. **Class Analytics & Statistics**: Calculates class averages, top performers, status distributions, and module completions.
7. **Class Report Exporter**: Writes structured class report card exports saved directly as `.txt` files.

---

## ⚙️ Quick Start Guide

### Prerequisites
- Python 3.8 or higher installed on your system.

### Running the OOP Demonstration Script (Requirements 1-5)
To execute the self-contained OOP student demo script showing class instantiations, progress percentages, and progress reports:
```bash
python demo.py
```

### Running the Interactive CLI Application
To run the full interactive student records management shell:
```bash
python run.py
```

### Running the Test Suite
To execute the automated unit checks (asserts CRUD operations, GPA calculations, and student methods):
```bash
python test_runner.py
```

---

## 📂 File Architecture

```
├── .gitignore
├── README.md              # Project manual
├── reflection.md          # Concept reflection report
├── run.py                 # CLI app entrypoint script
├── demo.py                # Self-contained OOP student program (assignment demo)
├── test_runner.py         # Automated unit test suite
├── students_db.json       # Local database storage (automatically created)
└── src/
    ├── __init__.py        # Src package marker
    ├── student.py         # Defines the OOP Student class and progress checks
    ├── main.py            # CLI menu interfaces and sub-menu workflows
    ├── student_manager.py # Student CRUD algorithms & statistical mathematics
    ├── file_handler.py    # Database I/O, backup buffers, and report exporters
    └── utils.py           # Validated input loops and ANSI terminal styling
```

---

## 🧬 Module 1 Concepts Map

The system uses standard core Python patterns:
- **Object-Oriented Coding**: Structuring student files inside custom classes and defining instance method behaviors (`src/student.py`).
- **Advanced Collections**: Storing student object models inside an email-keyed dictionary mapping, and lists of strings for modules tracking (`demo.py`, `src/student_manager.py`).
- **Loops & Control**: Multi-layered nested `while` menus, conditionals matching inputs, and conditional status routing (`src/main.py`, `src/student_manager.py`).
- **Exceptions (`try/except`)**: Enforcing decimal constraints for grades and numeric boundaries for ages without program termination (`src/utils.py`).
- **File I/O**: Context managers (`with open`) reading/writing JSON records and printing text streams (`src/file_handler.py`).

---

## 🚀 Pushing to GitHub (For Grading)

To satisfy the **GitHub & README** portion of the rubric, this project was built using a local Git repository with structured commits. Follow these steps to link this project to your GitHub:

1. **Create a new, empty repository** on GitHub.
2. **Copy your GitHub repository URL** (e.g., `https://github.com/your-username/student-record-system.git`).
3. Open your terminal in this project directory and run the following commands:
   ```bash
   # Add your GitHub repository link as the remote origin
   git remote add origin <PASTE_YOUR_GITHUB_REPOSITORY_URL>
   
   # Rename the default branch to main
   git branch -M main
   
   # Push your local commits to GitHub
   git push -u origin main
   ```
4. Verify that your commits and README appear on your GitHub repository page.
