"""
MAJOR PROJECT ASSIGNMENT
Database Management System Using Python & SQLite

Project: Course Enrollment Management System
Interface: Command Line (CLI)
Requirements covered:
- SQLite database created automatically
- Related tables with primary keys and foreign keys
- User registration, login, and logout
- Admin and Staff role-based authorization
- CRUD operations for student and course records
- Student-course enrollment and enrollment status updates
- SQL CREATE, INSERT, SELECT, UPDATE, DELETE operations
- Input validation and exception handling
- Functions, variables, conditionals, loops, lists/tuples/dictionaries
- Password hashing using Python's standard library

How to run:
    python DBMS_Major_Project.py

Demo accounts:
    Admin: admin / admin123
    Staff: staff / staff123

Only this .py file is required to start the program. On first run, it creates
course_enrollment.db automatically in the same working directory.

Educational project only. Change demo passwords before real deployment.
"""

import sqlite3
import hashlib
import os
from getpass import getpass

DB_NAME = "course_enrollment.db"


def hash_password(password):
    """Return a salted PBKDF2 hash rather than storing a plain-text password."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return salt.hex() + "$" + digest.hex()


def verify_password(password, stored):
    try:
        salt_hex, digest_hex = stored.split("$", 1)
        salt = bytes.fromhex(salt_hex)
        check = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
        return check.hex() == digest_hex
    except (ValueError, TypeError):
        return False


def connect_db():
    """Create/connect to database and enable foreign-key enforcement."""
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                created_by INTEGER,
                FOREIGN KEY(created_by) REFERENCES users(user_id)
                    ON DELETE SET NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL UNIQUE,
                fee REAL NOT NULL CHECK(fee >= 0),
                duration TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                enrollment_date TEXT NOT NULL DEFAULT (date('now')),
                status TEXT NOT NULL DEFAULT 'Active'
                    CHECK(status IN ('Active', 'Completed', 'Cancelled')),
                UNIQUE(student_id, course_id),
                FOREIGN KEY(student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE,
                FOREIGN KEY(course_id) REFERENCES courses(course_id)
                    ON DELETE RESTRICT
            )
        """)
        # Demo users are inserted only when they do not already exist.
        for username, password, role in (
            ("admin", "admin123", "admin"),
            ("staff", "staff123", "staff"),
        ):
            exists = conn.execute(
                "SELECT 1 FROM users WHERE username = ?", (username,)
            ).fetchone()
            if not exists:
                conn.execute(
                    "INSERT INTO users(username, password_hash, role) VALUES (?, ?, ?)",
                    (username, hash_password(password), role),
                )


def prompt_nonempty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def prompt_int(label, minimum=1):
    while True:
        raw = input(label).strip()
        try:
            value = int(raw)
            if value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f"Enter a whole number greater than or equal to {minimum}.")


def prompt_fee(label):
    while True:
        raw = input(label).strip()
        try:
            value = float(raw)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid non-negative amount.")


def login():
    print("\n--- Login ---")
    username = prompt_nonempty("Username: ")
    password = getpass("Password: ")
    with connect_db() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    if user and verify_password(password, user["password_hash"]):
        print(f"\nWelcome, {username}! Role: {user['role'].upper()}")
        return dict(user)
    print("Invalid username or password.")
    return None


def register_user():
    print("\n--- Staff Registration ---")
    username = prompt_nonempty("Choose username: ")
    password = getpass("Choose password (minimum 6 characters): ")
    if len(password) < 6:
        print("Password must contain at least 6 characters.")
        return
    with connect_db() as conn:
        try:
            conn.execute(
                "INSERT INTO users(username, password_hash, role) VALUES (?, ?, 'staff')",
                (username, hash_password(password)),
            )
            print("Staff account created successfully.")
        except sqlite3.IntegrityError:
            print("That username already exists.")


def add_student(user_id):
    name = prompt_nonempty("Student full name: ")
    email = prompt_nonempty("Email: ").lower()
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        print("Please enter a valid email address.")
        return
    phone = prompt_nonempty("Phone: ")
    with connect_db() as conn:
        try:
            conn.execute(
                "INSERT INTO students(full_name, email, phone, created_by) VALUES (?, ?, ?, ?)",
                (name, email, phone, user_id),
            )
            print("Student added successfully.")
        except sqlite3.IntegrityError:
            print("This email is already registered.")


def list_students():
    with connect_db() as conn:
        rows = conn.execute("""
            SELECT s.student_id, s.full_name, s.email, s.phone,
                   u.username AS created_by
            FROM students s
            LEFT JOIN users u ON u.user_id = s.created_by
            ORDER BY s.student_id
        """).fetchall()
    print("\n--- Students ---")
    if not rows:
        print("No student records found.")
        return
    for row in rows:
        print(f"ID: {row['student_id']} | {row['full_name']} | "
              f"{row['email']} | {row['phone']} | Added by: {row['created_by'] or 'N/A'}")


def update_student():
    student_id = prompt_int("Student ID to update: ")
    with connect_db() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
        if not row:
            print("Student ID not found.")
            return
        name = input(f"Full name [{row['full_name']}]: ").strip() or row["full_name"]
        email = input(f"Email [{row['email']}]: ").strip().lower() or row["email"]
        phone = input(f"Phone [{row['phone']}]: ").strip() or row["phone"]
        try:
            conn.execute(
                "UPDATE students SET full_name = ?, email = ?, phone = ? WHERE student_id = ?",
                (name, email, phone, student_id),
            )
            print("Student updated successfully.")
        except sqlite3.IntegrityError:
            print("That email belongs to another student.")


def delete_student():
    student_id = prompt_int("Student ID to delete: ")
    with connect_db() as conn:
        row = conn.execute(
            "SELECT full_name FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()
        if not row:
            print("Student ID not found.")
            return
        confirm = input(f"Delete {row['full_name']} and their enrollments? (y/n): ").strip().lower()
        if confirm == "y":
            conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            print("Student and related enrollment records deleted.")
        else:
            print("Delete cancelled.")


def add_course():
    name = prompt_nonempty("Course name: ")
    fee = prompt_fee("Course fee: ")
    duration = prompt_nonempty("Duration (e.g., 6 months): ")
    with connect_db() as conn:
        try:
            conn.execute(
                "INSERT INTO courses(course_name, fee, duration) VALUES (?, ?, ?)",
                (name, fee, duration),
            )
            print("Course added successfully.")
        except sqlite3.IntegrityError:
            print("That course already exists.")


def list_courses():
    with connect_db() as conn:
        rows = conn.execute("SELECT * FROM courses ORDER BY course_id").fetchall()
    print("\n--- Courses ---")
    if not rows:
        print("No course records found.")
        return
    for row in rows:
        print(f"ID: {row['course_id']} | {row['course_name']} | "
              f"Fee: ₹{row['fee']:.2f} | Duration: {row['duration']}")


def update_course():
    course_id = prompt_int("Course ID to update: ")
    with connect_db() as conn:
        row = conn.execute(
            "SELECT * FROM courses WHERE course_id = ?", (course_id,)
        ).fetchone()
        if not row:
            print("Course ID not found.")
            return
        name = input(f"Course name [{row['course_name']}]: ").strip() or row["course_name"]
        fee_text = input(f"Course fee [{row['fee']}]: ").strip()
        duration = input(f"Duration [{row['duration']}]: ").strip() or row["duration"]
        try:
            fee = float(fee_text) if fee_text else row["fee"]
            if fee < 0:
                raise ValueError
            conn.execute(
                "UPDATE courses SET course_name = ?, fee = ?, duration = ? WHERE course_id = ?",
                (name, fee, duration, course_id),
            )
            print("Course updated successfully.")
        except ValueError:
            print("Invalid fee. Course was not updated.")
        except sqlite3.IntegrityError:
            print("That course name already exists.")


def delete_course():
    course_id = prompt_int("Course ID to delete: ")
    with connect_db() as conn:
        row = conn.execute(
            "SELECT course_name FROM courses WHERE course_id = ?", (course_id,)
        ).fetchone()
        if not row:
            print("Course ID not found.")
            return
        try:
            conn.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
            print("Course deleted successfully.")
        except sqlite3.IntegrityError:
            print("Cannot delete this course because enrollment records refer to it.")


def enroll_student():
    list_students()
    student_id = prompt_int("Student ID: ")
    list_courses()
    course_id = prompt_int("Course ID: ")
    with connect_db() as conn:
        try:
            conn.execute(
                "INSERT INTO enrollments(student_id, course_id) VALUES (?, ?)",
                (student_id, course_id),
            )
            print("Enrollment created successfully.")
        except sqlite3.IntegrityError as exc:
            print("Could not enroll. Check IDs, or this student may already be enrolled.")
            print(f"Details: {exc}")


def list_enrollments():
    with connect_db() as conn:
        rows = conn.execute("""
            SELECT e.enrollment_id, s.full_name, c.course_name,
                   e.enrollment_date, e.status
            FROM enrollments e
            JOIN students s ON s.student_id = e.student_id
            JOIN courses c ON c.course_id = e.course_id
            ORDER BY e.enrollment_id
        """).fetchall()
    print("\n--- Enrollments ---")
    if not rows:
        print("No enrollment records found.")
        return
    for row in rows:
        print(f"Enrollment ID: {row['enrollment_id']} | Student: {row['full_name']} | "
              f"Course: {row['course_name']} | Date: {row['enrollment_date']} | "
              f"Status: {row['status']}")


def update_enrollment_status():
    enrollment_id = prompt_int("Enrollment ID: ")
    status = prompt_nonempty("New status (Active/Completed/Cancelled): ").title()
    if status not in {"Active", "Completed", "Cancelled"}:
        print("Invalid status.")
        return
    with connect_db() as conn:
        cursor = conn.execute(
            "UPDATE enrollments SET status = ? WHERE enrollment_id = ?",
            (status, enrollment_id),
        )
        print("Enrollment status updated." if cursor.rowcount else "Enrollment ID not found.")


def staff_menu(user):
    while True:
        print("""
--- STAFF MENU ---
1. Add student
2. View students
3. View courses
4. Enroll student in course
5. View enrollments
6. Update enrollment status
7. Logout
""")
        choice = input("Choose option: ").strip()
        try:
            if choice == "1":
                add_student(user["user_id"])
            elif choice == "2":
                list_students()
            elif choice == "3":
                list_courses()
            elif choice == "4":
                enroll_student()
            elif choice == "5":
                list_enrollments()
            elif choice == "6":
                update_enrollment_status()
            elif choice == "7":
                print("Logged out.")
                return
            else:
                print("Invalid menu selection.")
        except sqlite3.Error as exc:
            print(f"Database error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to main menu.")
            return


def admin_menu(user):
    while True:
        print("""
--- ADMIN MENU ---
1. Add student
2. View students
3. Update student
4. Delete student
5. Add course
6. View courses
7. Update course
8. Delete course
9. Enroll student in course
10. View enrollments
11. Update enrollment status
12. Register staff account
13. Logout
""")
        choice = input("Choose option: ").strip()
        try:
            if choice == "1":
                add_student(user["user_id"])
            elif choice == "2":
                list_students()
            elif choice == "3":
                update_student()
            elif choice == "4":
                delete_student()
            elif choice == "5":
                add_course()
            elif choice == "6":
                list_courses()
            elif choice == "7":
                update_course()
            elif choice == "8":
                delete_course()
            elif choice == "9":
                enroll_student()
            elif choice == "10":
                list_enrollments()
            elif choice == "11":
                update_enrollment_status()
            elif choice == "12":
                register_user()
            elif choice == "13":
                print("Logged out.")
                return
            else:
                print("Invalid menu selection.")
        except sqlite3.Error as exc:
            print(f"Database error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to main menu.")
            return


def main():
    try:
        initialize_db()
        while True:
            print("""
========================================
 COURSE ENROLLMENT MANAGEMENT SYSTEM
========================================
1. Login
2. Register staff account
3. Exit
""")
            choice = input("Choose option: ").strip()
            if choice == "1":
                user = login()
                if user:
                    if user["role"] == "admin":
                        admin_menu(user)
                    else:
                        staff_menu(user)
            elif choice == "2":
                register_user()
            elif choice == "3":
                print("Thank you for using the system.")
                break
            else:
                print("Invalid menu selection.")
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed.")
    except sqlite3.Error as exc:
        print(f"Database initialization error: {exc}")


if __name__ == "__main__":
    main()
