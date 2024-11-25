import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.filedialog import askopenfilename
import pandas as pd

# Global variables to store user information and attempts
username = ""
password = ""
login_attempts = 3
student_attempts = 3

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


def clear_gui():
    for widget in window.winfo_children():
        widget.destroy()


def show_welcome_screen():
    clear_gui()
    welcome_label = tk.Label(window, text="Welcome to Humber College", font=("Corbel", 24, "bold"), bg="#FDF4E7")
    welcome_label.pack(pady=100)
    
    # Display the welcome message for 3 seconds, then go to account creation
    window.after(3000, create_account)


def create_account():
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

    clear_gui()

    tk.Label(window, text="Create User Account", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)

    # Username field
    tk.Label(window, text="Enter a username:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5)
    username_entry = tk.Entry(window, width=40)  
    username_entry.pack(pady=5)

    # Password field
    tk.Label(window, text="Enter a password:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5)
    password_entry = tk.Entry(window, show="*", width=40)  
    password_entry.pack(pady=5)

    # Password instructions
    instruction_bullet_points = """
    Password must:
    - Be at least 10 characters long
    - Contain at least 1 uppercase letter
    - Contain 2 or 3 numbers
    - Contain 1 special character
    """
    tk.Label(window, text=instruction_bullet_points, justify="left", font=("Corbel", 10), bg="#FFFFFF", width=33).pack(pady=10)

    # Submit button
    tk.Button(window, text="Create Account", font=("Corbel", 12, "bold"), bg="#000000", fg="#FDF4E7",command=lambda: submit_account(username_entry, password_entry), width=25, height=1).pack(pady=10)


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
    def validate_login(login_username_entry, login_password_entry):
        global login_attempts

        login_username = login_username_entry.get()
        login_password = login_password_entry.get()

        # Check if username and password match the stored values
        if login_username == username and login_password == password:
            messagebox.showinfo("Success", "Login successful!")
            get_student_count()
        else:
            login_attempts -= 1  # Decrement remaining attempts
            if login_attempts > 0:
                messagebox.showerror("Error", f"Invalid credentials. {login_attempts} attempt(s) remaining.")
            else:
                messagebox.showerror("Error", "You have exceeded the maximum login attempts.")
                window.quit()  # Lock the user out since they have exceeded 3 tries

    clear_gui()

    tk.Label(window, text="Login", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)

    # Username field
    tk.Label(window, text="Enter your username:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5)
    login_username_entry = tk.Entry(window, width=40)  
    login_username_entry.pack(pady=5)

    # Password field
    tk.Label(window, text="Enter your password:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5)
    login_password_entry = tk.Entry(window, show="*", width=40)  
    login_password_entry.pack(pady=5)

    # Login button
    tk.Button(window, text="Login", font=("Corbel", 12, "bold"), bg="#000000", fg="#FDF4E7", command=lambda: validate_login(login_username_entry, login_password_entry), width=25, height=1).pack(pady=10)


def get_student_count():
    global student_attempts

    def validate_student_count():
        global student_attempts

        try:
            num_students = int(student_entry.get())
            if 1 <= num_students <= 50:
                enter_student_names(num_students)
            else:
                student_attempts -= 1
                if student_attempts > 0:
                    messagebox.showerror("Invalid Input", f"Please enter a number between 1 and 50. {student_attempts} attempt(s) remaining.")
                else:
                    messagebox.showinfo("Input Failed", "Too many incorrect attempts.")
                    window.quit()
        except ValueError:
            student_attempts -= 1
            messagebox.showerror("Invalid Input", "Please enter a valid number. {student_attempts} attempt(s) remaining.")
            if student_attempts == 0:
                messagebox.showinfo("Input Failed", "Too many incorrect attempts.")
                window.quit()


    clear_gui()

    tk.Label(window, text="Student Count", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)

    student_label = tk.Label(window, text="Enter the number of students (1-50):", font=("Corbel", 12), bg="#FDF4E7")
    student_label.pack(pady=10)

    global student_entry
    student_entry = tk.Entry(window, width=40) 
    student_entry.pack(pady=5)

    validate_button = tk.Button(window, text="Submit", bg="#000000", fg="#FDF4E7", font=("Corbel", 12, "bold"), command=validate_student_count, width=25, height=1)
    validate_button.pack(pady=10)


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

    clear_gui()
    tk.Label(window, text="Student Names", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)

    name_entries = []
    for i in range(num_students):
        tk.Label(window, text=f"Enter name of Student {i + 1}:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5)
        name_entry = tk.Entry(window, width=40) 
        name_entry.pack(pady=5)
        name_entries.append(name_entry)

    submit_button = tk.Button(window, text="Submit", bg="#000000", fg="#FDF4E7", font=("Corbel", 12, "bold"), command=submit_names, width=25, height=1)
    submit_button.pack(pady=10)


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
            
            # Check for mismatches in student names
            file_student_names = set(data["Student Name"])
            provided_student_names = set(student_names)
        
            # Find missing or extra names
            missing_names = provided_student_names - file_student_names
            extra_names = file_student_names - provided_student_names

            if missing_names:
                messagebox.showerror(
                    "Missing Students",
                    f"The following students are missing in the file: {', '.join(missing_names)}"
                )
                get_student_count()
                return
            
            if extra_names:
                messagebox.showerror(
                    "Extra Students",
                    f"The file contains students not in the provided list: {', '.join(extra_names)}"
                )
                get_student_count()
                return
                
            # Convert data to a two-dimensional list
            student_data = []
            for _, row in data.iterrows():
                grades = [int(row[course]) for course in CREDIT_HOURS.keys()]
                if not all(0 <= grade <= 100 for grade in grades):
                    messagebox.showerror("Invalid Grades", "Grades must be between 0 and 100.")
                    return
                student_data.append([row["Student Name"]] + grades)
            
            calculate_gpa(student_data)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    clear_gui()
    tk.Label(window, text="Upload Grades", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)

    # Add instructions for the file upload
    tk.Label(window, text="Please upload a valid Excel (.xlsx) or CSV (.csv) file with the following format:", font=("Corbel", 10), bg="#FDF4E7").pack(pady=10)

    # Display the expected file format
    example_text = (
        "Student Name\tMath\tScience\tLanguage\tDrama\tMusic\tBiology\n\n"
        "ABC\t\t85\t90\t78\t88\t92\t84\n"
        "XYZ\t\t88\t87\t89\t90\t88\t98"
    )

    tk.Label(window, text=example_text, font=("Corbel", 10), bg="#FFFFFF", justify="left").pack(pady=10)

    upload_button = tk.Button(window, text="Upload", bg="#000000", fg="#FDF4E7", font=("Corbel", 12, "bold"), command=process_file, width=25, height=1)
    upload_button.pack(pady=20)


def calculate_gpa(student_data):
    results = []

    for row in student_data:
        name = row[0]
        grades = row[1:]  # All columns after the name are grades
        weighted_sum = sum(grades[i] * list(CREDIT_HOURS.values())[i] for i in range(len(grades)))
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

    clear_gui()
    display_results(results)


def display_results(results):
    result_text = ""
    for name, gpa, school in results:
        result_text += f"Student: {name}\nGPA: {gpa:.2f}\nSchool: {school}\n\n"

    result_label = tk.Label(window, text=result_text, justify=tk.LEFT, bg="#FDF4E7")
    result_label.pack()


def main():
    global window

    # Create main window
    window = tk.Tk()
    window.title("Student Grades Management")
    window.configure(bg="#FDF4E7")
    window.wm_state('zoomed')

    # Start with the welcome screen
    show_welcome_screen()
    window.mainloop()


main()
