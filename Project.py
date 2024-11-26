import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
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
    tk.Label(window, text="Student Names", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=10)

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(window, bg="#FDF4E7")
    frame.pack(fill="both", expand=True, pady=10)

    canvas = tk.Canvas(frame, bg="#FDF4E7")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Link the scrollbar to the canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    content_frame = tk.Frame(canvas, bg="#FDF4E7")
    canvas.create_window((0, 0), window=content_frame, anchor="center")

    # Add student name entry fields inside the content frame
    name_entries = []
    for i in range(num_students):
        tk.Label(content_frame, text=f"Enter name of Student {i + 1}:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5, anchor="center", padx=500)
        name_entry = tk.Entry(content_frame, width=40)
        name_entry.pack(pady=5, padx=500)
        name_entries.append(name_entry)

    # Add submit button outside the scrollable area
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
    school_distribution = {
        "School of Engineering": 0,
        "School of Business": 0,
        "Law School": 0,
        "Not accepted": 0
    }

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
        school_distribution[school] += 1

    clear_gui()
    display_reports(results, school_distribution)


def display_reports(results, school_distribution):

    def generate_report_content(report_number):
        # Generate the selected report content
        if report_number == 1:
            report_content = "Student Name\t|\tSchool Name\n"
            report_content += "\n".join(f"{name}\t \t{school}" for name, _, school in results)
        elif report_number == 2:
            accepted_count = sum(v for k, v in school_distribution.items() if k != "Not accepted")
            report_content = f"Total Number of Accepted Students: {accepted_count}\n\n"
            report_content += "Distribution per School:\n"
            report_content += "\n".join(f"{school}: {count}" for school, count in school_distribution.items() if school != "Not accepted")
        elif report_number == 3:
            not_accepted_count = school_distribution["Not accepted"]
            report_content = f"Number of Students Rejected: {not_accepted_count}\n"
        elif report_number == 4:
            borderline_students = []
            # Define GPA thresholds for borderline cases
            borderline_ranges = {
                "School of Engineering": (89, 90),
                "School of Business": (79, 80),
                "Law School": (69, 70)
            }
            # Loop through results to find borderline students who are not accepted
            for name, gpa, assigned_school in results:
                for school, (low, high) in borderline_ranges.items():
                    if low <= gpa <= high:
                        closest_school = school
                        borderline_students.append((name, gpa, high, closest_school))

            if borderline_students:
                report_content = "Student Name    | GPA   | Required GPA    | Closest Cutoff School\n"
                for student in borderline_students:
                    name, gpa, high, closest_school = student
                    report_content += f"{name:<15} | {gpa:<4.2f} | {high:<14.2f}  | {closest_school}\n"
            else:
                report_content = "No students are borderline for any school."
        show_report(report_content, results, school_distribution)
    clear_gui()

    # Buttons for each report
    tk.Label(window, text="Select a Report to View", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)
    
    tk.Button(window, text="Student Names and Schools", font=("Corbel", 12, "bold"), command=lambda: generate_report_content(1), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Accepted Student Distribution", font=("Corbel", 12, "bold"), command=lambda: generate_report_content(2), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Rejected Students", font=("Corbel", 12, "bold"), command=lambda: generate_report_content(3), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Borderline Rejected Students", font=("Corbel", 12, "bold"), command=lambda: generate_report_content(4), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Redo Report Generation", font=("Corbel", 12, "bold"), command=get_student_count, bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)

def show_report(report_content, results, school_distribution):

    clear_gui()
    tk.Label(window, text="Report Content", font=("Corbel", 24, "bold"),bg="#FDF4E7").pack(pady=50)

    # Text widget to display the report content
    text_widget = tk.Text(window, font=("Courier New", 10), bg="#FFFFFF", wrap="none", width=70, height=15)
    text_widget.insert("1.0", report_content)
    text_widget.config(state="disabled")
    text_widget.pack(pady=10)

    # Download Report button
    def download_report():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Report As"
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(report_content)
            messagebox.showinfo("Success", f"Report saved to {file_path}")

    tk.Button(window, text="Download Report", font=("Corbel", 12, "bold"), command=download_report, bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=20)
    tk.Button(window, text="Back", font=("Corbel", 12, "bold"), command=lambda: display_reports(results, school_distribution), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=20)

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
