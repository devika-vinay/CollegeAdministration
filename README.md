# 🎓 College Administration App  

A Python-based Tkinter GUI application for managing student accounts, grades, and admissions decisions. The app simulates an academic administration tool with features for account creation, login, student enrollment, grade uploads, GPA calculation, and reporting.  

---

## 🔍 Features  

- **Account Management**  
  - Welcome splash screen with timed transition.  
  - User account creation with password strength rules (≥10 chars, 1 uppercase, 2–3 numbers, 1 special character).  
  - Secure login system with limited attempts.  

- **Student Data Input**  
  - Collect number of students (1–50) with validation.  
  - Enter student names with scrollable UI.  

- **Grade Upload & Validation**  
  - Upload grades from `.xlsx` or `.csv` files.  
  - File validation ensures expected columns 
  - Detects missing or extra student names.  
  - Validates grade ranges (0–100).  

- **GPA Calculation & Admissions Logic**  
  - Weighted GPA computed using predefined credit hours.  
  - Students divided into various admission categories for different schools  

- **Reports**  
  - Student-to-school allocation.  
  - Accepted student distribution by school.  
  - Count of rejected students.  
  - Borderline cases of students close to admission thresholds
  - Option to **redo reports** for a new student batch.  
  - Export reports to `.txt` files.  

---

## 📊 Insights  

- A **rule-based GPA system** maps students into acceptance tiers, highlighting how academic weighting can impact admission opportunities.  
- The **borderline report** adds nuance by surfacing students just below cutoffs, allowing administrators to consider conditional offers.  
- Validation at every stage (passwords, student counts, grade files) reduces errors and enforces data consistency.  

---

## 💡 Enhancements

- **Enhance security**: Hash and store passwords instead of holding them in memory.  
- **Add persistence**: Save student data and admissions decisions to a database rather than in-memory only.  
- **Expand flexibility**: Allow administrators to configure credit hours, grade thresholds, and acceptance criteria.  
- **Modernize UI**: Upgrade to a more scalable framework for broader usability.  

---

## 🛠️ Tech Stack  

- **Language**: Python  
- **GUI**: Tkinter  
- **Data Processing**: Pandas  
- **File I/O**: CSV, Excel (.xlsx), TXT export  

---

## 📂 Project Notes  

- Code references GeeksforGeeks, StackOverflow, and Pythontutorial.net for UI patterns and file handling.  
- Designed for educational purposes as part of an academic project.  

---
