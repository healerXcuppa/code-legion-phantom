#   IDEAS FOR LOOPS:
# - Multiplication table (user picks number, loop prints 1-12)
# - Number guessing game (loop until user guesses correctly)
# - Sum calculator (loop until user enters 0)
# - Countdown timer (loop from 10 down to 1)
# - List printer (loop through your favorite items)

# """Idea 1: Multiplication Table"""
# print(f"\n{'='*10} Multiplication Table Generator {'='*10}\n")
# num1 = int(input("Enter first number: "))
# num2 = int(input("\nEnter the number of rows to display: "))
# for num in range(num2):
#     print(f"{num1} x {num+1} = {num1 * (num+1)}")

"""Idea 2: Number Guessing game"""
# print(f"\n{'='*5}Number Guessing Game{'='*5}\n")
# guess = 6
# guess_count = 0
# print("ONLY 3 GUESSES.\n")
# while True:
#     guess_num = int(input("Enter your guess: "))
#     guess_count += 1
#     if guess_count == 3:
#         print("You are out of guesses!!!")
#         break
#     elif guess_num == guess:
#         print("Congrats!! You got the guess right.")
#         break
#     elif guess_num < guess:
#         print("Guess number is greater than your guessed number.")
#     elif guess_num > guess:
#         print("Guess Number is lesser than Guessed number.")
#     else:
#         print("Invalid input.")

# """Idea 3: Simple Sum Calculator"""
# print(f"\n{'='*20} Sum Calculator {'='*20}\n")
# while True:
#     num_sum = 0
#     num_count = int(input("How many numbers do you want to sum up?\n Answer >>> "))
#     if num_count == 0:
#         print(f"{'='*20} Calculator Closed {'='*20}\n")
#         break
#     print("\nSum NUmbers:\n")
#     for num in range(num_count):
#         num_assign = input("Enter the number to sum: ")
#         num_sum += float(num_assign)
#     print(f"\nThe sum of the numbers is: {num_sum}")
#     print(f"{'='*20}{'='*20}\n")

# """Idea 4: Countdown Timer"""
import time
print(f"\n{'='*20} Countdown Timer {'='*20}")
retry_count = 0
# Main program loop
while True:
    try:
        # Get and validate countdown value
        set_countdown = int(input("\nEnter the number of seconds to countdown: "))

        while set_countdown < 0:
            print("\nCoutdown must only be positive values.\n")
            retry_count += 1
            if retry_count == 3:
                time.sleep(0.5)
                print(f"\n{'='*20}Countdown Timer automatically shutdown.{'='*20}\n")
                break
            set_countdown = int(input("Enter a positive number: "))
        if retry_count == 3:
            break

        #Iteration of the countdown value
        for num in range(set_countdown,-1,-1):
            time.sleep(1)
            print(num)
        time.sleep(0.5)
        print("\nCountdown Session Ended Successfully.\n")
        
        #Checing if user wants to have another countdown session
        retry_count = 0
        tryAgain_list = ("no","n","yes","y")
        try_again_retry = 0
        time.sleep(1)
        tryAgain = input(f"Do you want to try again? \n Options = {tryAgain_list}\n Answer >>> ").lower().strip()
        
        #Error handling for user invalid inputs during Try Again session
        while tryAgain not in tryAgain_list:
            try_again_retry += 1
            print("\nInvalid input. Please choose from the options: ", tryAgain_list)
            if try_again_retry == 3:
                print(f"\n{'='*20}Countdown Timer automatically shutdown.{'='*20}\n")
                break
            tryAgain = input(f"Do you want to try again? \n Options = {tryAgain_list}\n Answer >>> ").lower().strip()

        #Main loop break after validation
        if try_again_retry == 3:
            break
        
        #User input validation for appropriate choices during Try Again session
        if tryAgain in tryAgain_list:
            if tryAgain in ("no","n"):
                time.sleep(0.5)
                print("\nCountdown Timer Closed.\n")
                break
            if tryAgain in ("yes","y"):
                time.sleep(0.5)
                print("\nCountdown Timer Restarted.\n")
                continue
    #Except ValueError block to check for string value inputs during the countdown value session
    except ValueError:
        retry_count +=1
        time.sleep(0.5)
        print("Input must be an integer or a number.")
        
        if retry_count == 3:
            time.sleep(0.5)
            print("\nCountdown Timer automatically shutdown.\n")
            break
time.sleep(1)
print(f"{'='*20}{'='*20}\n")
#Adding other IDEAS soon...,

# """Idea 5: List Printer"""
# print(f"\n{'='*20} List Printer {'='*20}\n")
# my_list = ["Python", "JavaScript", "C++", "Java", "Ruby"]
# for index, item in enumerate(my_list):
#     print(f"{index+1}. {item}")
# print(f"\n{'='*20}{'='*20}")