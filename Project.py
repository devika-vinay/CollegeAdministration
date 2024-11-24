# prompt: When the program starts, a welcoming message will appear “Welcome in Humber
# College”
# 2- Allow the user to login using a password. The password must satisfy the following rules:
# • Should not be less than 10 characters.
# • Should contain at least one upper case letter.
# • Should contain two or three numbers.
# • Should contain one special character.
# If the password is incorrect, the system must ask the user to enter new password. The
# system must allow the user only three attempts.
# If the password is correct, the system will continue
# 3- After password checking, the system must ask the user to enter the number of students,
# the number must be between 1-50. If the user enters any other number, the system must
# inform the user to enter a correct number (i.e., between 1-50). The system must allow the
# user only three attempts otherwise the program will stop.
# Use python GUI for all of the above

import tkinter as tk
import tkinter.messagebox as messagebox
import re

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
          messagebox.showinfo("Login Failed","Too many incorrect password attempts")
          window.destroy()
    else:
        messagebox.showinfo("Success", "Login Successful!")
        password_label.config(text="")
        password_entry.config(state=tk.DISABLED)
        login_button.config(state=tk.DISABLED)
        get_student_count()

def get_student_count():
    def validate_student_count():
        try:
            num_students = int(student_entry.get())
            if 1 <= num_students <= 50:
                messagebox.showinfo("Success","Number of students validated.")
                window.destroy() # or proceed to the next stage
            else:
                attempts_left_students.set(attempts_left_students.get() - 1)
                messagebox.showerror("Invalid Input", "Please enter a number between 1 and 50.")
                if attempts_left_students.get() == 0:
                    messagebox.showinfo("Input Failed", "Too many incorrect attempts. Program stopping.")
                    window.destroy()
        except ValueError:
            attempts_left_students.set(attempts_left_students.get()-1)
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            if attempts_left_students.get()==0:
                messagebox.showinfo("Input Failed","Too many incorrect attempts. Program stopping.")
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
    attempts_label = tk.Label(window, textvariable=attempts_left_students)
    attempts_label.pack()
    

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
attempts_label = tk.Label(window, textvariable=attempts_left)
attempts_label.pack()

window.mainloop()
