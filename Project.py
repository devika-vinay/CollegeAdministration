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
credit_hours = [("Math", 4), ("Science", 5), ("Language", 4), ("Drama", 3), ("Music", 2), ("Biology", 4)]
total_credits = sum(credits for subject, credits in credit_hours)

# Create main window
window = tk.Tk()

# Clearing GUI window by iterating through all child widgets and destroying them
# Reference: https://www.geeksforgeeks.org/how-to-clear-out-a-frame-in-the-tkinter/
def clearGUI():
    for widget in window.winfo_children():
        widget.destroy()


def showWelcomeScreen():
    welcome_label = tk.Label(window, text="Welcome to Humber College", font=("Corbel", 24, "bold"), bg="#FDF4E7")
    welcome_label.pack(pady=100)
    
    # Display the welcome message for 3 seconds, then go to account creation
    # Reference: https://www.geeksforgeeks.org/python-after-method-in-tkinter/
    window.after(3000, createAccount)

# Additional functionality for user to create their account before they login
def createAccount():

    # Using nested functions for readability and increased variable scope of GUI components such as username_entry and password_entry
    # Reference: https://www.geeksforgeeks.org/python-inner-functions/
    def submitAccount(username_entry, password_entry):

        # Setting values for global variables, username and password
        global username, password
        username = username_entry.get()
        password = password_entry.get()

        # Check username and password validity with popup dialog boxes for errors and successes using messagebox
        # Reference: https://www.tutorialspoint.com/how-to-create-a-tkinter-error-message-box
        if not username.strip():
            messagebox.showerror("Error", "Username cannot be empty")
            return

        error = checkPasswordValidity()
        if error:
            messagebox.showerror("Error", error)
        else:
            messagebox.showinfo("Success", "Account created successfully!")
            login()

    # Clearing GUI after each screen is complete
    clearGUI()

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

    # Submit button using lambda functions to pass arguments in a function when button is pressed
    # Reference: https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
    tk.Button(window, text="Create Account", font=("Corbel", 12, "bold"), bg="#000000", fg="#FDF4E7",command=lambda: submitAccount(username_entry, password_entry), width=25, height=1).pack(pady=10)


def checkPasswordValidity():
    # Check password validity based on given rules
    numcount=0
    uppercasecount=0
    specialcharcount=0
    for char in password:
        if char.isupper():
            uppercasecount+=1
        if not (char.isalpha() or char.isdigit() or char == ' '):
            specialcharcount+=1
        if char.isdigit():
            numcount+=1

    if len(password) < 10:
        return "Password should not be less than 10 characters."
    if uppercasecount < 1:
        return "Password should contain at least one uppercase letter."
    if specialcharcount < 1:
        return "Password should contain at least one special character."
    if numcount not in [2, 3]:  
        return "Password should contain only two or three numbers."        
    return None


def login():
    def validateLogin(login_username, login_password):
        global login_attempts

        # Check if username and password match the stored values
        if login_username == username and login_password == password:
            messagebox.showinfo("Success", "Login successful!")
            getStudentCount()
        else:
            login_attempts -= 1  # Decrement remaining attempts
            if login_attempts > 0:
                messagebox.showerror("Error", f"Invalid credentials. {login_attempts} attempt(s) remaining.")
            else:
                messagebox.showerror("Error", "You have exceeded the maximum login attempts.")
                window.quit()  # Lock the user out since they have exceeded 3 tries

    #Clearing existing screen before displaying login screen
    clearGUI()

    tk.Label(window, text="Login", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)

    # Username field
    tk.Label(window, text="Enter your username:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5)
    login_username_entry = tk.Entry(window, width=40)  
    login_username_entry.pack(pady=5)

    # Password field
    tk.Label(window, text="Enter your password:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5)
    login_password_entry = tk.Entry(window, show="*", width=40)  
    login_password_entry.pack(pady=5)

    # Login button calling nested function validateLogin with parameters using lambda functions
    tk.Button(window, text="Login", font=("Corbel", 12, "bold"), bg="#000000", fg="#FDF4E7", command=lambda: validateLogin(login_username_entry.get(), login_password_entry.get()), width=25, height=1).pack(pady=10)


def getStudentCount():
    global student_attempts

    def validateStudentCount():
        global student_attempts
        num_students = int(student_entry.get())

        # Check if user input string is a number and between 1 and 50, else show error popups
        if not student_entry.get().isdigit():
            student_attempts -= 1
            if student_attempts > 0:
                messagebox.showerror("Invalid Input", f"Please enter a number between 1 and 50. {student_attempts} attempt(s) remaining.")
            else:
                messagebox.showinfo("Input Failed", "Too many incorrect attempts.")
                window.quit()
        elif 1 <= num_students <= 50:
            enterStudentNames(num_students)
        else:
            student_attempts -= 1
            if student_attempts > 0:
                messagebox.showerror("Invalid Input", f"Please enter a number between 1 and 50. {student_attempts} attempt(s) remaining.")
            else:
                messagebox.showinfo("Input Failed", "Too many incorrect attempts.")
                window.quit()

    # Clearing existing screen before dislpaying student count screen
    clearGUI()

    tk.Label(window, text="Student Count", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)

    student_label = tk.Label(window, text="Enter the number of students (1-50):", font=("Corbel", 12), bg="#FDF4E7")
    student_label.pack(pady=10)

    student_entry = tk.Entry(window, width=40) 
    student_entry.pack(pady=5)

    validate_button = tk.Button(window, text="Submit", bg="#000000", fg="#FDF4E7", font=("Corbel", 12, "bold"), command=validateStudentCount, width=25, height=1)
    validate_button.pack(pady=10)


def enterStudentNames(num_students):
    student_names = []

    def submitNames():

        # Obtaining names from GUI entries and checking if empty, then show error popups, else appending names to list
        for i in range(num_students):
            name = name_entries[i].get().strip()
            if name == "":
                messagebox.showerror("Invalid Input", f"Name for Student {i + 1} cannot be empty.")
                return
            student_names.append(name)
        uploadGrades(student_names)

    # Clearing existing screen before displaying student names screen
    clearGUI()
    tk.Label(window, text="Student Names", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=10)

    # Creating canvas within window to contain a frame
    canvas = tk.Canvas(window, bg="#FDF4E7")

    # Initializing frame to create a scrollable region in the canvas
    # Reference: https://pythoneo.com/creating-scrollable-interfaces-with-tkinter/
    frame = tk.Frame(canvas, bg="#FDF4E7")

    # Creating a vertical scrollbar linked to the canvas.
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(fill="both", expand="true")

    # Placing the frame within the canvas at 0,0 position anchored at top left
    canvas.create_window((0, 0), window=frame, anchor="nw")

    name_entries = []
    for i in range(num_students):
        tk.Label(frame, text=f"Enter name of Student {i + 1}:", font=("Corbel", 12), bg="#FDF4E7").pack(pady=5, anchor="center", padx=500)
        name_entry = tk.Entry(frame, width=40)
        name_entry.pack(pady=5, padx=500)
        name_entries.append(name_entry)

    submit_button = tk.Button(frame, text="Submit", bg="#000000", fg="#FDF4E7", font=("Corbel", 12, "bold"), command=submitNames, width=25, height=1)
    submit_button.pack(pady=10)

    # Define the scrollable region within the frame after all contents have been added
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))


def uploadGrades(student_names):
    def processFile():
        # Using askopenfilename to allow user to select a single file of the specified file type using a dialog box
        # Reference: https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
        filename = askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")], title="Select a file with grades")

        # Go back if file path is empty
        if not filename:
            return
        
        # Try catch block to catch unexpected errors
        try:
            # Read file based on its extension
            # Reference: https://www.geeksforgeeks.org/reading-excel-file-using-python/
            if filename.endswith('.xlsx'):
                data = pd.read_excel(filename)
            elif filename.endswith('.csv'):
                data = pd.read_csv(filename)
            else:
                messagebox.showerror("Invalid File", "Please upload a valid Excel or CSV file.")
                return
            
            # Ensure file has correct structure
            expected_columns = ["Student Name"] + list(subject for subject, credits in credit_hours)
            if not all(col in data.columns for col in expected_columns):
                messagebox.showerror("Invalid File", f"File must contain the following columns: {', '.join(expected_columns)}")
                return
            
            # Check for mismatches in student names using dataframe
            # Reference: https://www.geeksforgeeks.org/get-a-list-of-a-particular-column-values-of-a-pandas-dataframe/
            # Reference: https://stackoverflow.com/questions/8866652/determine-if-2-lists-have-the-same-elements-regardless-of-order
            file_student_names = set(data["Student Name"])
            provided_student_names = set(student_names)
        
            # Find missing or extra names
            missing_names = provided_student_names - file_student_names
            extra_names = file_student_names - provided_student_names

            if missing_names:
                messagebox.showerror("Missing Students", f"The following students are missing in the file: {', '.join(missing_names)}")
                getStudentCount()
                return
            
            if extra_names:
                messagebox.showerror("Extra Students", f"The file contains students not in the provided list: {', '.join(extra_names)}")
                getStudentCount()
                return
                
            # Convert data to a two-dimensional list by iterating over dataframe
            # Reference: https://www.geeksforgeeks.org/different-ways-to-iterate-over-rows-in-pandas-dataframe/
            student_data = []
            subject_list = list(subject for subject, credit in credit_hours)
            for index, row in data.iterrows():
                grades = [int(row[subject]) for subject in subject_list]
                if not all(0 <= grade <= 100 for grade in grades):
                    messagebox.showerror("Invalid Grades", "Grades must be between 0 and 100.")
                    return
                student_data.append([row["Student Name"]] + grades)

            calculateGpa(student_data)
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    clearGUI()
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

    upload_button = tk.Button(window, text="Upload", bg="#000000", fg="#FDF4E7", font=("Corbel", 12, "bold"), command=processFile, width=25, height=1)
    upload_button.pack(pady=20)


def calculateGpa(student_data):
    results = []
    school_distribution = [("School of Engineering", 0), ("School of Business", 0), ("Law School", 0), ("Not accepted", 0)]

    # Calculating gpa for students and appending to a list with their name, gpa and accepted school
    for row in student_data:
        name = row[0]
        grades = row[1:]  # All columns after the name are grades
        weighted_sum = sum(grades[i] * credit_hours[i][1] for i in range(len(grades)))

        gpa = weighted_sum / total_credits
        if 90 <= gpa <= 100:
            school = "School of Engineering"
        elif 80 <= gpa < 90:
            school = "School of Business"
        elif 70 <= gpa < 80:
            school = "Law School"
        else:
            school = "Not accepted"
        results.append((name, gpa, school))
        
        # Update school distribution
        for i in range(len(school_distribution)):
            if school_distribution[i][0] == school:
                school_distribution[i] = (school_distribution[i][0], school_distribution[i][1] + 1)
                break

    clearGUI()
    displayReports(results, school_distribution)


def displayReports(results, school_distribution):

    def generateReportContent(report_number):
        # Generate the selected report content
        if report_number == 1:
            # Generate report for students and their allocated schools using list comprehension
            report_content = "Student Name\t|\tSchool Name\n"
            report_content += "\n".join(f"{name}\t \t{school}" for name, gpa, school in results)

        elif report_number == 2:
            # If student is NOT in "Not Accepted" category, count them
            accepted_count = sum(count for school, count in school_distribution if school != "Not accepted")
            report_content = f"Total Number of Accepted Students: {accepted_count}\n\n"
            report_content += "Distribution per School:\n"
            report_content += "\n".join(f"{school}: {count}" for school, count in school_distribution if school != "Not accepted")

        elif report_number == 3:
            # Get number of unaccepted students by referencing index of not accepted from the list of school distibutions
            not_accepted_count = school_distribution[3][1]
            report_content = f"Number of Students Rejected: {not_accepted_count}\n"

        elif report_number == 4:
            ''' Displays a report of the students who nearly missed the acceptance criteria for each school, thereby allowing
            administrators to offer conditional acceptance/late acceptance'''
            borderline_students = []
            # Define GPA thresholds for borderline cases
            borderline_ranges = [("School of Engineering", 89, 90), ("School of Business", 79, 80), ("Law School", 69, 70)]

            # Loop through results to find borderline students who are not accepted
            for name, gpa, assigned_school in results:
                for school, low, high in borderline_ranges:
                    if low <= gpa <= high:
                        closest_school = school
                        borderline_students.append((name, gpa, high, closest_school))
            
            # Sort students into order based on the school
            engineering_students = []
            business_students = []
            law_students = []

            for i in range(len(borderline_students)):
                if borderline_students[i][3] == "School of Engineering":
                    engineering_students.append(borderline_students[i])
                elif borderline_students[i][3] == "School of Business":
                    business_students.append(borderline_students[i])
                elif borderline_students[i][3] == "Law School":
                    law_students.append(borderline_students[i])
            
            ordered_list_students = engineering_students + business_students + law_students


            # Compile the report format from the content in the borderline_students list
            if ordered_list_students:
                report_content = "Student Name    | GPA   | Required GPA    | Closest Cutoff School\n"
                for student in ordered_list_students:
                    name, gpa, high, closest_school = student
                    report_content += f"{name:<15} | {gpa:<4.2f} | {high:<14.2f}  | {closest_school}\n"
            else:
                report_content = "No students are borderline for any school."
        showReport(report_content, results, school_distribution)
    clearGUI()

    # Buttons for each report using lambda functions for those that need arguments
    tk.Label(window, text="Select a Report to View", font=("Corbel", 24, "bold"), bg="#FDF4E7").pack(pady=50)
    
    tk.Button(window, text="Student Names and Schools", font=("Corbel", 12, "bold"), command=lambda: generateReportContent(1), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Accepted Student Distribution", font=("Corbel", 12, "bold"), command=lambda: generateReportContent(2), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Rejected Students", font=("Corbel", 12, "bold"), command=lambda: generateReportContent(3), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Borderline Rejected Students", font=("Corbel", 12, "bold"), command=lambda: generateReportContent(4), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)
    tk.Button(window, text="Redo Report Generation", font=("Corbel", 12, "bold"), command=getStudentCount, bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=10)

def showReport(report_content, results, school_distribution):

    clearGUI()
    tk.Label(window, text="Report Content", font=("Corbel", 24, "bold"),bg="#FDF4E7").pack(pady=50)

    # Text widget to display the report content in the top left of the widget in a read only state
    # Reference: https://www.geeksforgeeks.org/python-tkinter-text-widget/
    text_widget = tk.Text(window, font=("Courier New", 10), bg="#FFFFFF", wrap="none", width=70, height=15)
    text_widget.insert("1.0", report_content)
    text_widget.config(state="disabled")
    text_widget.pack(pady=10)

    # Download Report button using a dialog box in the specified format
    # Reference: https://www.geeksforgeeks.org/python-asksaveasfile-function-in-tkinter/
    def download_report():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Save Report As"
        )

        # Open the file path to write report content and show success popup
        if file_path:
            with open(file_path, "w") as file:
                file.write(report_content)
            messagebox.showinfo("Success", f"Report saved to {file_path}")

    tk.Button(window, text="Download Report", font=("Corbel", 12, "bold"), command=download_report, bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=20)
    tk.Button(window, text="Back", font=("Corbel", 12, "bold"), command=lambda: displayReports(results, school_distribution), bg="black", fg="#FDF4E7", width=25, height=1).pack(pady=20)

def main():
    # Reference global window
    global window 
    window.title("Student Grades Management")

    # Set background colour and set window size to full screen
    # Reference: https://stackoverflow.com/questions/24404729/tkinter-window-with-both-title-bar-and-windows-taskbar
    window.configure(bg="#FDF4E7")
    window.state("zoomed")

    # Start with the welcome screen
    showWelcomeScreen()
    window.mainloop()


main()
