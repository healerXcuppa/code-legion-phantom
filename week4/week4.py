"""Week 4: Building a calculator using functions"""
import shutil
import os
import time

width = shutil.get_terminal_size().columns

def intro():
    """Prints Out The Intro"""
    os.system('cls' if os.name == "nt" else 'clear')
    print(f"{'='*width}")
    print("PHANTOM CALCULATOR (Type 'exit' to stop Calculator)".center(width))
    print(f"{'='*width}")

def show_menu():
    """Prints Out The Menu"""
    menu = [
        "1. Calculator",
        "2. Calculation History",
        "3. Exit"
    ]
    for item in menu:
        print(item)

def pause_and_clear():
    """Pause and clear screen when called"""
    time.sleep(1)
    os.system('cls' if os.name == "nt" else 'clear')

calc_history = []
def history():
    """History of Calculations"""
    for index, value in enumerate(calc_history):
        print(f"{index + 1}. {value}")

    time.sleep(1)
    input("\nPress Enter to continue...")
    pause_and_clear()

def add(a,b):
    """Returns Sum"""
    result = f"({a} + {b}) = {a + b}"
    calc_history.append(result)
    print(f"\n{result}")

def minus(a,b):
    """Returns Difference"""
    result = f"({a} - {b}) = {a - b}"
    calc_history.append(result)
    print(f"\n{result}")
    
def product(a,b):
    """Returns Product"""
    result = f"({a} * {b}) = {a * b}"
    calc_history.append(result)
    print(f"\n{result}")
    
def divide(a,b):
    """Returns Divident"""
    try:
        result = f"({a} / {b}) = {a / b}"
        calc_history.append(result)
        print(f"\n{result}")
    except ZeroDivisionError:
        print("\nError: Cannot divide by zero!")
    
def modulo(a,b):
    """Returns Remainder"""
    result = f"({a} % {b}) = {a % b}"
    calc_history.append(result)
    print(f"\n{result}")
    
operators = ( "+" , "-" , "/" , "*" , "%" )

while True:
    intro()
    show_menu()
    try:
        choice = int(input("\nEnter your choice: ").lower().strip())
        
        if choice == 3:
            pause_and_clear()
            break
        
        if choice == 2:
            os.system('cls' if os.name == "nt" else 'clear')
            print(f"{'='*width}")
            print("PHANTOM CALCULATOR HISTORY".center(width))
            print(f"{'='*width}")
            history()
        
        if choice == 1:
            while True:
                intro()
                
                # 1. Loop until a valid first number is provided
                while True:
                    raw_num1 = input("\nEnter first number: ").lower().strip()
                    if raw_num1 == "exit":
                        break
                    try:
                        num1 = int(raw_num1)
                        break # Success! Break out of the first number loop
                    except ValueError:
                        print("Input must be a number or 'exit'.")
                
                # If they typed exit, drop out to the main menu
                if raw_num1 == "exit":
                    pause_and_clear()
                    break
                    
                # 2. Loop until a valid second number is provided
                while True:
                    raw_num2 = input("\nEnter Second number: ").lower().strip()
                    if raw_num2 == "exit":
                        break
                    try:
                        num2 = int(raw_num2)
                        break # Success! Break out of the second number loop
                    except ValueError:
                        print("Input must be a number or 'exit'.")
                
                if raw_num2 == "exit":
                    pause_and_clear()
                    break

                # 3. Loop until a valid operator is provided
                while True:
                    operation = input("\nEnter the operation sign to perform calculation: ").strip()
                    if operation in operators:
                        break
                    print(f"\nWrong operator. Select an operator {operators}")

                # --- PERFORM CALCULATION ---
                if operation == "+":
                    add(num1, num2)
                elif operation == "-":
                    minus(num1, num2)
                elif operation == "*":
                    product(num1, num2)
                elif operation == "/":
                    divide(num1, num2)
                else:
                    modulo(num1, num2)

                # Let the user see the answer before looping back!
                input("\nPress Enter to continue...")
                
    except ValueError:
        print("Invalid input. Please enter a valid menu number (1, 2, or 3).")
        pause_and_clear()