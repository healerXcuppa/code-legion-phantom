"""Day 3: Variable MManipulation and String Operations"""
#Variable and string value
name = "Abdul-Malik Mohammed Salis"

#setting operations
uppercase = name.upper()    #Changing all text or string values to uppercase.
lowercase = name.lower()    #Changing all text or string values to lowercase.
title = name.capitalize()  #Title format by making only the first letters of every word uppercase.
count = len(name)   #counting the number of elements in the variable {name} value. This includes the spacing inbetween words.

#printing operands and commands -- Main assignment.
print(f"\nMy name is {name}.")
print(f"\nName written in only uppercase is {uppercase}.")
print(f"\nName in lowercase is {lowercase}.")
print(f"The title format of the name is {title}.")
print(f"\nThe length of the characters in the variable name value is {count}.")

#Bonus Question -- Slicing first and last 3 letters
first = name[0:3]
last = name[-3:]
print(f"\nThe first three letters sliced from the name are {first}.")
print(f"\nThe last thre letters in the name variable are {last}.")