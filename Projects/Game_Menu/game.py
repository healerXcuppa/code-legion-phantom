"""Building a Program with 2 games"""
# Imported Libraries
import time
import random
import os

#Main Loop for Program
player_wins = 0
computer_wins = 0
retry_mainLoop = 0
while True:
    try:
        #Creating Main Game Menu and looping through with enumeration.
        time.sleep(2)
        print("MAIN MENU BOOTING...")
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(1.5)
        
        #Using the below block to displayh the Main Menu of the program
        print(f"\n{'='*15} MAIN MENU {'='*15}")
        game_menu = ["Rock, Paper, Scissors", "Countdown Timer", "Exit"]
        for index, game in enumerate(game_menu):
            print(f"{index + 1}. {game}")
        time.sleep(1.5)
        
        main_MenuInput = int(input("\nEnter a selection. (Must be the menu number.)\n choice >>> "))

        #Error Handling for negative and greater values input for Main Menu loop
        if main_MenuInput not in (1,2,3):
            retry_mainLoop += 1

            # Breaking loop after validating error limit in main menu
            if retry_mainLoop == 3:
                time.sleep(1)
                print("User out of menu retries.")
                time.sleep(0.5)
                print("\n Program shutdown")
                print(f"\n{'='*20}{'='*20}")
                break
            
            #This runs when the user's retry main loop is not equal to 0
            time.sleep(0.25)
            print("\nInvalid menu option.\n")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nPlease select must select within menu number (1 to 3)")
            time.sleep(0.5)
            print("\nProgram Refreshing....")
            print("Loading...")
            time.sleep(4)
            os.system('cls' if os.name == 'nt' else 'clear')
        
        #Main Loop break when the retry count reaches 3 by negative value input
        if retry_mainLoop == 3:
            break

        #Creating Menu Option Selection Validations and Loops
        if main_MenuInput == 3:
            time.sleep(0.5)
            print("Main Menu closing...")
            time.sleep(0.25)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(1.5)
            print("\nMain Menu Closed.")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        
        # Main Menu Option 1 loop for starting the Rock, Paper, Scissors Game
        #This is to select the RPS game from the main menu.
        if main_MenuInput == 1:
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(0.5)
            print("Menu 1: Rock, Paper, Scissors Starting")
            time.sleep(2)
            os.system('cls' if os.name == 'nt' else 'clear')

            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(1)
            print("\nRULES OF THE GAME:")
            time.sleep(1.5)
            print("\nRule 1: To select a game choice, Enter the option number")
            time.sleep(1)
            print("\nRule 2: Enter '0' to end game sequential round.")
            time.sleep(1)
            print("\nRule 3: Player has 3 error pardons if user make persistent error 3 times game exits to RPS menu.")
            time.sleep(2)
            print("\nGAME STARTING.....")
            time.sleep(5)
            os.system('cls' if os.name == 'nt' else 'clear')

            #When the RPS is selected, this should keep on repeating
            game1_menuRetry = 0
            while main_MenuInput == 1:
                print(f"{'='*10} ROCK, PAPER, SCISSORS GAME {'='*10}")
                game1_menuList = ("Start", "Leaderboard", "Exit")
                game1_choices = ("Rock","Paper","Scissors",)
                print("\nRPS Menu Options:")
                for rps, rps_menu in enumerate(game1_menuList):
                    print(f"{rps +1}. {rps_menu}")
                
                try:
                    time.sleep(1)
                    # game1_menuList selection == ("Start", "Leaderboard", "Exit")
                    game1_menuChoice = int(input("\nEnter a menu option to continue: "))

                    # Checking Validation issue for invalid range of menu options
                    if game1_menuChoice not in (1,2,3):
                        game1_menuRetry += 1    #Adds 1 to the RPS menu list retry count
                        
                        if game1_menuRetry == 3:    #Exexuting a task when the RPS menu limit is up
                            time.sleep(1)
                            print("\nUser out of RPS Menu retries.")
                            time.sleep(1)
                            print("RPS Menu automatically closing....")
                            time.sleep(2)
                            os.system('cls' if os.name == 'nt' else 'clear')
                            time.sleep(1)
                            print("Rock, Paper, Scissors Game Menu Closed.\nRPS Menu Closed.")
                            time.sleep(2)
                            os.system('cls' if os.name == 'nt' else 'clear')
                            break

                        #The below continues if only the above execution block doesn't validate meaning the RPS menu limit is not up
                        time.sleep(0.1)
                        print("\nInvalid menu option.")
                        time.sleep(1)
                        print("Enter a valid menu option to continue.")
                        time.sleep(1.5)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        
                        if game1_menuRetry == 3:    #Exits RPS to main menu when the RPS menu retry limit is up
                            break
                    
                    if game1_menuChoice == 3: # Exiting the RPS Menu using the exit game option.
                        time.sleep(0.5)
                        print("\nExiting RPS Menu...")
                        time.sleep(0.5)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break
                        
                    # RPS menu Option 2 for Leaderboard Statistics
                    if game1_menuChoice == 2:
                        time.sleep(0.2)
                        print("\nRPS Leaderboard Opening...")
                        time.sleep(0.5)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"{'='*15}RPS Leaderboard{'='*15}")
                        time.sleep(0.5)
                        print(f"\nComputer Win Count: {computer_wins}"'\n'f"Player Win Count: {player_wins}")

                        # Option for user to go back to RPS Menu after checking the leaderboard statistics and validating the user input for going back to RPS menu
                        time.sleep(1.5)
                        go_back = input("\n# to go back to RPS Main Menu: ")
                        
                        if go_back == "#":
                            time.sleep(0.25)
                            print("Going back to the RPS Menu")
                            time.sleep(2)
                            os.system('cls' if os.name == 'nt' else 'clear')
                        else:
                            break

                    # Selecting the start menu option in the RPS menu
                    mainGame1_retry = 0
                    while game1_menuChoice == 1:
                        time.sleep(1)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        try:
                            # RPS MENU OPTIONS DISPLAY
                            print("Enter menu option: ")    
                            for i, rps_choice in enumerate(game1_choices):
                                print(f"{i+1}. {rps_choice}")
                            time.sleep(1.5)
                            print("Enter 0 to end game")  

                            player_choice = int(input("\nEnter the menu number to select your game choice :\n Answer >>> ")) # Player selects from the menu options by entering the menu number or choice and validating the user input for the game choices
                            
                            if player_choice not in (0,1,2,3):    #Checking for invalid menu options
                                mainGame1_retry +=1
                                
                                if mainGame1_retry == 3:
                                    print("\nError Limit Reached. Game terminating....")
                                    time.sleep(0.25)
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    break
                                
                                time.sleep(1)
                                print("\nInvalid input. Please select from the menu options.")

                            if mainGame1_retry == 3:
                                break
                            
                            # Player choice to return to RPS Menu
                            if player_choice == 0:
                                time.sleep(1)
                                print("\nPlayer Terminated Game")
                                time.sleep(2)
                                os.system('cls' if os.name == 'nt' else 'clear')
                                break
                            
                            computer_choice = random.choice(game1_choices) # Computer randomly selects from the game choices list
                            print(f"\nComputer selected: {computer_choice}")

                            # Comparing Computer Choice and Player Choice to determine the winner of the round and validating the user input for the game choices and validating the error limit for invalid game choice inputs
                            if (computer_choice == "Rock" and player_choice == 1) or \
                                (computer_choice == "Paper" and player_choice == 2) or \
                                (computer_choice == "Scissors" and player_choice == 3):
                                time.sleep(1)
                                print("Tied")
                            elif (computer_choice == "Rock" and player_choice == 3) or \
                                (computer_choice == "Paper" and player_choice == 1) or\
                                (computer_choice == "Scissors" and player_choice == 2):
                                computer_wins += 1
                                time.sleep(1)
                                print("Computer Wins.")
                            else:
                                player_wins += 1
                                time.sleep(1)
                                print("Player Wins.")
                        
                        except ValueError:
                            mainGame1_retry += 1

                            if mainGame1_retry == 3:
                                time.sleep(1)
                                print("User Reponse Invalid")
                                time.sleep(1)
                                print("Game End.")
                                time.sleep(2)
                                os.system('cls' if os.name == 'nt' else 'clear')
                            
                            time.sleep(1)
                            print("User input must be menu number")

                except ValueError:
                    game1_menuRetry += 1 #This line is for validating the error limit for invalid menu option inputs in RPS Menu

                    if game1_menuRetry == 3:    # Validating the error limit for invalid menu option inputs in RPS Menu
                        time.sleep(1)
                        print("User out of RPS Menu retries.")
                        time.sleep(1.5)
                        print("\n\nRPS Menu automatically closing....")
                        time.sleep(1)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Rock, Paper, Scissors Game Menu Closed.")
                        time.sleep(1.5)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        break
                    
                    time.sleep(1)
                    print("\nInvalid input. Please select from the menu options.")
                    time.sleep(1.5)
                    os.system('cls' if os.name == 'nt' else 'clear')


        if main_MenuInput == 2:
            time.sleep(1.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(1)
            print("Menu 2: Countdown Timer")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(2)
            print(f"\n{'='*20} Countdown Timer {'='*20}")
            
            retry_count = 0
            # Main program loop
            while True:
                try:
                    # Get and validate countdown value
                    set_countdown = int(input("\nEnter the number of seconds to countdown: "))

                    while set_countdown < 0:
                        retry_count += 1

                        if retry_count == 3:
                            time.sleep(0.5)
                            print(f"\n{'='*20}Countdown Timer automatically shutdown.{'='*20}\n")
                            break
                        
                        time.sleep(1)
                        print("\nCoutdown must only be positive values.\n")
                        time.sleep(1)
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

                        if try_again_retry == 3:
                            print(f"\n{'='*20}Countdown Timer automatically shutdown.{'='*20}\n")
                            break

                        print("\nInvalid input. Please choose from the options: ", tryAgain_list)
                        tryAgain = input(f"\nDo you want to try again? \n Options = {tryAgain_list}\n Answer >>> ").lower().strip()

                    #Main loop break after validation
                    if try_again_retry == 3:
                        break
                    
                    #User input validation for appropriate choices during Try Again session
                    if tryAgain in tryAgain_list:
                        
                        if tryAgain in ("no","n"):
                            time.sleep(0.5)
                            print("\nCountdown Timer Closed.\n")
                            time.sleep(1.5)
                            os.system('cls' if os.name == 'nt' else 'clear')
                            time.sleep(1)
                            print("Going Back to Main Menu.")
                            time.sleep(2)
                            os.system('cls' if os.name == 'nt' else 'clear')
                            break

                        if tryAgain in ("yes","y"):
                            time.sleep(0.5)
                            print("\nCountdown Timer Restarted.\n")
                            continue

                #Except ValueError block to check for string value inputs during the countdown value session
                except ValueError:
                    retry_count +=1
                    
                    if retry_count == 3:
                        time.sleep(0.5)
                        print("\nCountdown Timer automatically shutdown.\n")
                        break
                    
                    time.sleep(0.5)
                    print("Input must be an integer or a number.")
            
    #Exception Block for string input by user
    except ValueError:
        retry_mainLoop += 1
        
        # Checking main program loop retry count to break program
        if retry_mainLoop == 3:
            time.sleep(0.3)
            print("\nUser out of menu retries.")
            time.sleep(0.1)
            print("\nProgram shutdown")
            break
        
        time.sleep(0.5)
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(1.5)
        print("\nString input detected.\nSelect a menu number")