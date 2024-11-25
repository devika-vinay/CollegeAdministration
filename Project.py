import tkinter as tk
import tkinter.messagebox as messagebox
import re

import pandas as pd  # For handling Excel/CSV files
from tkinter.filedialog import askopenfilename

def upload_grades(student_names):
    def process_file():
        file_path = askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title="Select a file with grades"
        )
        if not file_path:
            return
        
        try:
            # Read file based on its extension
            if file_path.endswith('.xlsx'):
                data = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                data = pd.read_csv(file_path)
            else:
                messagebox.showerror("Invalid File", "Please upload a valid Excel or CSV file.")
                return
            
            # Ensure file has correct structure
            expected_columns = ["Student Name"] + list(CREDIT_HOURS.keys())
            if not all(col in data.columns for col in expected_columns):
                messagebox.showerror(
                    "Invalid File",
                    f"File must contain the following columns: {', '.join(expected_columns)}"
                )
                return
            
            # Match grades to students
            student_grades = []
            for name in student_names:
                student_row = data[data["Student Name"] == name]
                if student_row.empty:
                    messagebox.showerror("Missing Data", f"No grades found for student: {name}")
                    return
                grades = [int(student_row[course].values[0]) for course in CREDIT_HOURS.keys()]
                if not all(0 <= grade <= 100 for grade in grades):
                    messagebox.showerror("Invalid Grades", "Grades must be between 0 and 100.")
                    return
                student_grades.append(grades)
            
            # Proceed to GPA calculation
            calculate_gpa(student_names, student_grades)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    # Clear the GUI and display the upload button
    clear_gui()
    upload_button = tk.Button(window, text="Upload Grades File", command=process_file)
    upload_button.pack()

def clear_gui():
    for widget in window.winfo_children():
        widget.destroy()

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
        upload_grades(student_names)

    name_entries = []

    for i in range(num_students):
        label = tk.Label(window, text=f"Enter name for Student {i + 1}:")
        label.pack()
        entry = tk.Entry(window)
        entry.pack()
        name_entries.append(entry)

    submit_button = tk.Button(window, text="Submit Names", command=submit_names)
    submit_button.pack()

'''def enter_student_grades(student_names):
    clear_gui()
    
    file_button = tk.Button(window, text="Upload Grades File", command=upload_grades(student_names))
    file_button.pack(pady=10)'''



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
