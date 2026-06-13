"""Day 7: Student Record with Loops (Upgraded to cover week 1 and 2)"""
print("\n============FILL STUDENT INFORMATION============\n")
student_name = input("Enter Student Name: ")
print("\nNB: STUDENT ID must be number only.")
student_ID = int(input("Enter STUDENT ID: "))
print("\nNB: STUDENT Grade/Level must be number only.")
print("NB: Total Grade(Level) = 16, So if in Level 100 type 13.")
grade_level = int(input("Enter your Grade/Level: "))
gpa = -1
while gpa < 0 or gpa > 4: #While loop to check gpa input error
    gpa = float(input("\nEnter GPA (0.0-4.0): "))
    if gpa < 0 or gpa > 4:
        print("Invalid! Try again. GPA must be (0.0-4.0)")
print(f"GPA recorded: {gpa}")
is_enrolled = True
lecturer_name = input("\nEnter the name of your lecturer: ")

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
credit_hours = [3, 4, 3, 3] #Added credit hour list
total_credit_hours = 0
subject_scores = [85, 72, 59, 91]   #Added subject scores list
extracurricular = ["Debate", "Hackathon", "Basketball"]
subjects.append("Risk Management")  # Adds "Risk Management" to the end of the subjects list
extracurricular.insert(0,"Football")    # Inserts Football at the beginning of the extracurricular list
subjects.pop(2) # Removes "Discrete Mathematics"
extracurricular[0]= "CTF's"
full_records_list = [student_name, student_ID, grade_level, gpa, subjects, extracurricular]
top_subjects = subjects[0:2]

#Output or Printing Statements
print("\n=============STUDENT RECORD===========\n")
print(f"Student Name: {student_name}")
print(f"Student Initial: {student_initial}")
print(f"Student ID: {student_ID}")
print(f"Grade Level: {grade_level}")
print(f"GPA: {gpa}({gpa_percentage})")
print(f"Enrolled: {is_enrolled}")

print("\n---ACADEMIC INFO---\n")
print(f"Honor Roll: {honor_roll}")
print(f"Upperclassman: {is_upperclassman}")
print(f"Needs Advisor: {needs_advisor}")
print(f"Can Graduate Early: {can_grad_early}")
print(f"Years Until Graduation: {grad_year}")
print(f"Credits Needed: {credits_needed}")
for credit_hour in credit_hours:
    total_credit_hours += credit_hour
print(f"Total Credit Hours: {total_credit_hours}")

print("\n--- COURSES ---\n")
#Added for loops to  use enumeration and parallel list control with Error handling for subject scroes
print("Subjects: ")
for count in range(len(subjects)):
    print(f"{count+1}. {subjects[count]} ----- {credit_hours[count]} credits ---- scores = {subject_scores[count]}/100")
for count in range(len(subjects)):
    if subject_scores[count] < 60:
        print(f"\nWARNING: Failing grade in: \n {subjects[count]} = {subject_scores[count]}/100")

print("\nTop Subjects: ")
for count, subject in enumerate(top_subjects,1):
    print(f"{count}. {subject}")

print("\nExtracurriculars: ")
for count, ext_curricular in enumerate(extracurricular,1):
    print(f"{count}. {ext_curricular}")

print("\n---CONTACT---\n")
print("Email: ", student_email)
print("Lecturer: ", lecturer_name)
print(f"Name Length: {name_length} characters")

print("\n---FULL RECORD---\n")
print(full_records_list)

print("\n========================")