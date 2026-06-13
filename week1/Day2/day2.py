"""Day 2:  Integers, Floats and Operations """

# Assigning Variables
num1 = int(input("\nEnter your first digit: "))
num2 = int(input("\nEnter your second digit: "))
num3 = float(input("\nEnter your third digit: "))
addition = int(num1 + num2 + num3)
multiplication = int(num1  * num2  * num3)
subtraction  = int(num1 - num2 - num3)
division = float(num1/num2/num3)

# Printing Commands
print(f"\nThe sum of the three numbers is: {addition}")
print(f"\n{multiplication} is the multiple of the three values")
print(f"\nThe value {subtraction} is the difference  between {num1}, {num2}, {num3}")
print(f"\n{division} is the value of the division of the input values")

# Bomus Section -- Finding the Rectandgle
length = float(input("\nEnnter the length of the rectangle: "))
breadth = float(input("\nEnter the width of the rectangle: "))
unit = input("\nEnter unit for rectangle.\n NB: Unit is always going to display in ^2: ")
area = length * breadth
print(f"\nThe area of the Rectangle is {area}{unit}^2")