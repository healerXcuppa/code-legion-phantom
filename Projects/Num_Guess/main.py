"""Creating a number Guessing Game 2 versions"""
# Version 1: NUMBER GUESSING GAME WITH GUESS CHANGING RANDOMLY AFTER EVERRY USER GUESS
import os
import time
import random
import shutil

width = shutil.get_terminal_size().columns

print()
print(f"{'='*width}")
print("Number Guessing Game (Use 'exit' to stop game)".center(width))
print(f"{'='*width}")

guess_range = 20
while True:
    computer_guess = random.randint(1,20)
    usr_guess = input("\nEnter your guess (Guess range between 1 and 20): ").lower().strip()
    
    if usr_guess == "exit":
        print("Game Closed!!")
        time.sleep(0.5)
        print("Goodbye!!")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        break
        
    usr_guess = int(usr_guess)
    time.sleep(1.5)
    print(f"Guess number is: {computer_guess}")
    
    if usr_guess > guess_range or usr_guess < 1:
        time.sleep(1)
        print("Out of guess range")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        break
    
    if usr_guess == computer_guess:
        time.sleep(0.5)
        print("\nYou guessed right.")
        print("Well Done!!!!")
    elif usr_guess > computer_guess:
        print("\nYour guess is greater than the number")
    elif usr_guess < computer_guess:
        print("\nThe guess is less than the number")

# Version 2: NUMBER GUESSING WITH GUESS LIMIT WITHOUT RANDOMIZATION UPON EVERY USER GUESS

# import os
# import time
# import random
# import shutil

# width = shutil.get_terminal_size().columns

# print()
# print(f"{'='*width}")
# print("Number Guessing Game (Use 'exit' to stop game)".center(width))
# print(f"{'='*width}")

# guess = random.randint(1,20)
# guess_trials = 3
# while True:
#     try:
#         user_guess = input(