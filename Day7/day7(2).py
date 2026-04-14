# ✨ IDEAS FOR LOOPS:
# - Multiplication table (user picks number, loop prints 1-12)
# - Number guessing game (loop until user guesses correctly)
# - Sum calculator (loop until user enters 0)
# - Countdown timer (loop from 10 down to 1)
# - List printer (loop through your favorite items)

"""Idea 1: Multiplication Table"""
print(f"\n{'='*10} Multiplication Table Generator {'='*10}\n")
num1 = int(input("Enter first number: "))
num2 = int(input("\nEnter the number of rows to display: "))
for num in range(num2):
    print(f"{num1} x {num+1} = {num1 * (num+1)}")

#Adding other IDEAS soon...