import tkinter as tk
import tkinter.messagebox as messagebox
import re

# Constants for credit hours
CREDIT_HOURS = {
    "Math": 4,
    "Science": 5,
    "Language": 4,
    "Drama": 3,
    "Music": 2,
    "Biology": 4
}
TOTAL_CREDIT_HOURS = sum(CREDIT_HOURS.values())

def clear_window():
    """Clears all widgets from the main window."""
    for widget in window.winfo_children():
        widget.destroy()

def check_password(password):
    """Checks if the password meets the specified criteria."""
    if len(password) < 10:
        return "Password must be at least 10 characters long."
    if not re.search("[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not (2 <= len(re.findall(r"\d", password)) <= 3):
        return "Password must contain two or three numbers."
    if not re.search("[^a-zA-Z0-9]", password):
        return "Password must contain at least one special character."
    return None  # Password is valid

def login():
    password = password_entry.get()
    error_message = check_password(password)
    if error_message:
        attempts_left.set(attempts_left.get() - 1)
        messagebox.showerror("Invalid Password", error_message)
        if attempts_left.get() == 0:
            messagebox.showinfo("Login Failed", "Too many incorrect password attempts")
            window.destroy()
    else:
        messagebox.showinfo("Success", "Login Successful!")
        clear_window()
        get_student_count()

def get_student_count():
    def validate_student_count():
        try:
            num_students = int(student_entry.get())
            if 1 <= num_students <= 50:
                messagebox.showinfo("Success", "Number of students validated.")
                clear_window()
                enter_student_names(num_students)
            else:
                attempts_left_students.set(attempts_left_students.get() - 1)
                messagebox.showerror("Invalid Input", "Please enter a number between 1 and 50.")
                if attempts_left_students.get() == 0:
                    messagebox.showinfo("Input Failed", "Too many incorrect attempts. Program stopping.")
                    window.destroy()
        except ValueError:
            attempts_left_students.set(attempts_left_students.get() - 1)
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            if attempts_left_students.get() == 0:
                messagebox.showinfo("Input Failed", "Too many incorrect attempts. Program stopping.")
                window.destroy()

    student_label = tk.Label(window, text="Enter the number of students (1-50):")
    student_label.pack(pady=10)

    global student_entry
    student_entry = tk.Entry(window)
    student_entry.pack()

    validate_button = tk.Button(window, text="Validate", command=validate_student_count)
    validate_button.pack(pady=5)

    global attempts_left_students
    attempts_left_students = tk.IntVar(value=3)
    attempts_label = tk.Label(window, text="Attempts Left:", textvariable=attempts_left_students)
    attempts_label.pack()

def enter_student_names(num_students):
    student_names = []

    def submit_names():
        for i in range(num_students):
            name = name_entries[i].get().strip()
            if not name:
                messagebox.showerror("Invalid Input", f"Name for Student {i + 1} cannot be empty.")
                return
            student_names.append(name)
        messagebox.showinfo("Success", "Student names recorded.")
        clear_window()
        enter_student_grades(student_names)

    name_entries = []

    for i in range(num_students):
        label = tk.Label(window, text=f"Enter name for Student {i + 1}:")
        label.pack()
        entry = tk.Entry(window)
        entry.pack()
        name_entries.append(entry)

    submit_button = tk.Button(window, text="Submit Names", command=submit_names)
    submit_button.pack()

def enter_student_grades(student_names):
    student_grades = []

    def submit_grades():
        for i, name in enumerate(student_names):
            grades = []
            for course in CREDIT_HOURS.keys():
                try:
                    grade = int(grade_entries[i][course].get())
                    if 0 <= grade <= 100:
                        grades.append(grade)
                    else:
                        messagebox.showerror("Invalid Grade", f"Grade for {course} must be between 0 and 100.")
                        return
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Grade for {course} must be a valid integer.")
                    return
            student_grades.append(grades)
        clear_window()
        calculate_gpa(student_names, student_grades)

    grade_entries = []

    for i, name in enumerate(student_names):
        label = tk.Label(window, text=f"Enter grades for {name}:")
        label.pack()
        entries = {}
        for course in CREDIT_HOURS.keys():
            course_label = tk.Label(window, text=f"{course}:")
            course_label.pack()
            entry = tk.Entry(window)
            entry.pack()
            entries[course] = entry
        grade_entries.append(entries)

    submit_button = tk.Button(window, text="Submit Grades", command=submit_grades)
    submit_button.pack()

def calculate_gpa(student_names, student_grades):
    results = []

    for i, name in enumerate(student_names):
        grades = student_grades[i]
        weighted_sum = sum(grade * CREDIT_HOURS[course] for grade, course in zip(grades, CREDIT_HOURS.keys()))
        gpa = weighted_sum / TOTAL_CREDIT_HOURS
        if 90 <= gpa <= 100:
            school = "School of Engineering"
        elif 80 <= gpa < 90:
            school = "School of Business"
        elif 70 <= gpa < 80:
            school = "Law School"
        else:
            school = "Not accepted"
        results.append((name, gpa, school))

    clear_window()
    display_results(results)

def display_results(results):
    result_text = ""
    for name, gpa, school in results:
        result_text += f"Student: {name}\nGPA: {gpa:.2f}\nSchool: {school}\n\n"

    result_label = tk.Label(window, text=result_text, justify=tk.LEFT)
    result_label.pack()

# Main window
window = tk.Tk()
window.title("Humber College")

welcome_label = tk.Label(window, text="Welcome to Humber College")
welcome_label.pack(pady=20)

password_label = tk.Label(window, text="Enter Password:")
password_label.pack()

password_entry = tk.Entry(window, show="*")
password_entry.pack()

login_button = tk.Button(window, text="Login", command=login)
login_button.pack(pady=10)

attempts_left = tk.IntVar(value=3)
attempts_label = tk.Label(window, text="Attempts Left:", textvariable=attempts_left)
attempts_label.pack()

window.mainloop()
