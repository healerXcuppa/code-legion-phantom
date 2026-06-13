"""Day 6: Simple Project Using Syntax from Day 1 -5 """
print("\n============FILL STUDENT INFORMATION============\n")
#Student Variables
student_name = input("Enter Student Name: ")
print("NB: STUDENT ID must be number only.")
student_ID = int(input("Enter STUDENT ID: "))
print("NB: STUDENT Grade/Level must be number only.")
print("NB: Total Grade(Level) = 16, So if in Level 100 type 13.")
grade_level = int(input("Enter your Grade/Level: "))
print("GPA range 0.00 - 4.00")
gpa = float(input("Enter your GPA: "))
is_enrolled = True
lecturer_name = input("Enter the name of your lecturer: ")

#Arithmetic Operations
grad_year = 16 - grade_level
gpa_percentage = (gpa/4.00)*100
credits_needed = (16 - grade_level)*42

#String Operations
student_initial = student_name[0].upper()
name_uppercase = student_name.upper()
name_length = len(student_name)
student_email = f"{student_name.split()[0].lower()}{student_ID}@school.edu"
student_summary = f"{student_name} (ID: {student_ID}) - Grade {grade_level}, GPA: {gpa}"
#Boolean Comparisons
honor_roll = gpa >= 3.5
is_upperclassman = grade_level >= 13
needs_advisor = gpa < 2.0 and is_enrolled
can_grad_early = grade_level == 16 and credits_needed <= 42

#List Operations
subjects = ["Linear Algebra", "Data Structures and Algorithms", "Discrete Mathematics", "System Analysis and Design"]
extracurricular = ["Debate", "Hackathon", "Basketball"]
subjects.append("Risk Management")  # Adds "Risk Management" to the end of the subjects list
extracurricular.insert(0,"Football")    # Inserts Football at the beginning of the extracurricular list
subjects.pop(2) # Removes "Discrete Mathematics"
extracurricular[0]= "CTF's"
full_records_list = [student_name, student_ID, grade_level, gpa, subjects, extracurricular]
top_subjects = subjects[0:2]

#Output or Printing Statements
print("\n=============STUDENT RECORD===========")
print(f"Student Name: {student_name}")
print(f"Student Initial: {student_initial}")
print(f"Student ID: {student_ID}")
print(f"Grade Level: {grade_level}")
print(f"GPA: {gpa}({gpa_percentage})")
print(f"Enrolled: {is_enrolled}")

print("\n---ACADEMIC INFO---")
print(f"Honor Roll: {honor_roll}")
print(f"Upperclassman: {is_upperclassman}")
print(f"Needs Advisor: {needs_advisor}")
print(f"Can Graduate Early: {can_grad_early}")
print(f"Years Until Graduation: {grad_year}")
print(f"Credits Needed: {credits_needed}")

print("\n--- COURSES ---")
print(f"Subjects: {subjects}")
print(f"Top Subjects: {top_subjects}")
print(f"Extracurriculars: {extracurricular}")

print("\n---CONTACT---")
print("Email: ", student_email)
print("Lecturer: ", lecturer_name)
print(f"Name Length: {name_length} characters")

print("\n---FULL RECORD---")
print(full_records_list)

print("\n========================")