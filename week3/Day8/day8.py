#Creating a Rock Paper Scissors Game.
"""Week 3(Day 8): Mastering Conditionals in Python."""
import random
print(f"{'='*10} ROCK, PAPER, SCISSORS GAME {'='*10}")
initiate = ["start", "stop"]
choices = ["rock","paper","scissors"]
computer_wins = 0
player_wins = 0
start_or_stop = input("\nType start or stop to end game: ").strip().lower()
while True:
    if start_or_stop not in initiate:
        print("Invalid input. Please type start to begin or stop to end the game.")
        start_or_stop = input("\nType start or stop to end game: ").strip().lower()
        continue
    elif start_or_stop == "stop":
        print("\nGame terminated")
        print(f"Computer Win Count: {computer_wins}"'\n'f"Player Win Count: {player_wins}")
        break

    if start_or_stop == "start":
        computer_choice = random.choice(choices).strip().lower()
        print("\nEnter your choice (rock, paper or scissors)\n")
        player_choice = input("Enter your selected option: ").strip().lower()
        if player_choice == "stop":
            print("Player Terminated Game")
            break
        print(f"Computer selected: {computer_choice}")
        if player_choice not in choices:
            for num in range(3):
                print("Input is not an option. Please try again.\n")
                player_choice = input("Enter your selected option: ").strip().lower()
                if player_choice in choices:
                    break
            else:
                print("Invalid input 3 times game automatically terminated.")
                break

        if computer_choice == player_choice:
            print("Tied")
        elif (computer_choice == "rock" and player_choice == "scissors") or \
            (computer_choice == "paper" and player_choice == "rock") or\
            (computer_choice == "scissors" and player_choice == "paper"):
            computer_wins += 1
            print("Computer Wins.")
        else:
            player_wins += 1
            print("Player Wins.")