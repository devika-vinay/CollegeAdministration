import tkinter as tk
import tkinter.messagebox as messagebox
import re
import pandas as pd
from tkinter.filedialog import askopenfilename

# Global variables to store user information and attempts
username = ""
password = ""
login_attempts = 3
student_attempts = 3

def show_welcome_screen():
    clear_gui()
    welcome_label = tk.Label(window, text="Welcome to Humber College", font=("Arial", 24, "bold"))
    welcome_label.pack(pady=100)
    
    # Display the welcome message for 3 seconds, then go to account creation
    window.after(3000, create_account)

def create_account():
    clear_gui()

    # Username field
    tk.Label(window, text="Enter a username:", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(window, width=40)  # Consistent width for text box
    username_entry.pack(pady=5)

    # Password field
    tk.Label(window, text="Enter a password:", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(window, show="*", width=40)  # Consistent width for text box
    password_entry.pack(pady=5)

    # Password instructions
    instruction_bullet_points = """
    Password must:
    - Be at least 10 characters long
    - Contain at least 1 uppercase letter
    - Contain 2 or 3 numbers
    - Contain 1 special character
    """
    tk.Label(window, text=instruction_bullet_points, justify="left", font=("Arial", 10)).pack(pady=10)

    # Submit button
    tk.Button(window, text="Submit", command=lambda: submit_account(username_entry, password_entry), width=20, height=2).pack(pady=10)

def submit_account(username_entry, password_entry):
    global username, password
    username = username_entry.get()
    password = password_entry.get()

    # Check username, password validity
    if not username.strip():
        messagebox.showerror("Error", "Username cannot be empty")
        return
    error = is_valid_password(password)
    if error:
        messagebox.showerror("Error", error)
    else:
        messagebox.showinfo("Success", "Account created successfully!")
        login()

def is_valid_password(password):
    # Check password validity based on given rules
    if len(password) < 10:
        return "Password should not be less than 10 characters."
    if not any(char.isupper() for char in password):
        return "Password should contain at least one uppercase letter."
    if len([char for char in password if char.isdigit()]) not in [2, 3]:
        return "Password should contain two or three numbers."
    if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/\\|" for char in password):
        return "Password should contain at least one special character."
    return None

def login():
    clear_gui()
    # Username field
    tk.Label(window, text="Enter your username:", font=("Arial", 12)).pack(pady=5)
    login_username_entry = tk.Entry(window, width=40)  # Consistent width for text box
    login_username_entry.pack(pady=5)

    # Password field
    tk.Label(window, text="Enter your password:", font=("Arial", 12)).pack(pady=5)
    login_password_entry = tk.Entry(window, show="*", width=40)  # Consistent width for text box
    login_password_entry.pack(pady=5)

    # Login button
    tk.Button(window, text="Login", command=lambda: validate_login(login_username_entry, login_password_entry), width=20, height=2).pack(pady=10)

def validate_login(login_username_entry, login_password_entry):
    global login_attempts

    login_username = login_username_entry.get()
    login_password = login_password_entry.get()

    # Check if username and password match the stored values
    if login_username == username and login_password == password:
        messagebox.showinfo("Success", "Login successful!")
        clear_gui()
        get_student_count()
    else:
        login_attempts -= 1  # Decrement remaining attempts
        if login_attempts > 0:
            messagebox.showerror("Error", f"Invalid credentials. {login_attempts} attempt(s) remaining.")
        else:
            messagebox.showerror("Error", "You have exceeded the maximum login attempts.")
            window.quit()  # Lock the user out since they have exceeded 3 tries

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
    upload_button = tk.Button(window, text="Upload Grades File", command=process_file, width=20, height=2)
    upload_button.pack(pady=20)

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

    student_label = tk.Label(window, text="Enter the number of students (1-50):", font=("Arial", 12))
    student_label.pack(pady=10)

    global student_entry
    student_entry = tk.Entry(window, width=40)  # Consistent width for text box
    student_entry.pack(pady=5)

    validate_button = tk.Button(window, text="Validate", command=validate_student_count, width=20, height=2)
    validate_button.pack(pady=10)

    global attempts_left_students
    attempts_left_students = tk.IntVar(value=3)
    attempts_label = tk.Label(window, text="Attempts Left:", textvariable=attempts_left_students, font=("Arial", 12))
    attempts_label.pack(pady=10)

def enter_student_names(num_students):
    student_names = []

    def submit_names():
        for i in range(num_students):
            name = name_entries[i].get().strip()
            if not name:
                messagebox.showerror("Invalid Input", f"Name for Student {i + 1} cannot be empty.")
                return
            student_names.append(name)
        upload_grades(student_names)
    
    name_entries = []
    for i in range(num_students):
        tk.Label(window, text=f"Enter name of Student {i + 1}:", font=("Arial", 12)).pack(pady=5)
        name_entry = tk.Entry(window, width=40)  # Consistent width for text box
        name_entry.pack(pady=5)
        name_entries.append(name_entry)

    submit_button = tk.Button(window, text="Submit Names", command=submit_names, width=20, height=2)
    submit_button.pack(pady=10)

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

# Create main window
window = tk.Tk()
window.title("Student Grades Management")

window.wm_state('zoomed')


# Start with the welcome screen
show_welcome_screen()

window.mainloop()
