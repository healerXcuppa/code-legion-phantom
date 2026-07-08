"""ATM SIMULATOR"""
import os
import shutil
import time

width = shutil.get_terminal_size().columns

def clear_screen():
    """Screen Clear Function"""
    time.sleep(1)
    os.system('cls' if os.name == "nt" else 'clear')

def print_header(title):
    """Prints out a header with the passed argument"""
    os.system('cls' if os.name == "nt" else 'clear')
    print()
    print(f"{'='*width}")
    print(title.center(width))
    print(f"{'='*width}")
    print()

def pause_and_clear():
    time.sleep(2)
    input("\nPress any key to return to the main menu...")
    clear_screen()

def show_menu():
    """Returns the ATM menu"""
    atm_menu_list = ["Check Balance","Deposit","Withdraw","Transaction History","Exit"]
    for menu_index,atm_menu_item in enumerate(atm_menu_list):
        print(f"{menu_index + 1}. {atm_menu_item}")

def check_balance():
    """Returns the current balance"""
    print_header("ACCOUNT BALANCE")
    print(f"\nYour current balance is: ${balance}")

def deposit():
    """Deposit money into the account"""
    print_header("DEPOSIT MENU")
    global balance
    try:
        deposit_amount = float(input("Enter amount to deposit: $"))
        if deposit_amount <= 0:
            print("\nDeposit amount must be greater than zero.")
        else:
            balance += deposit_amount
            print(f"\nSuccessfully deposited ${deposit_amount}. New balance is: ${balance}")
            transaction_history.append(f"Deposit: +${deposit_amount}")
    except ValueError:
        print("\nInvalid input. Please enter a valid amount.")

def withdraw():
    """Withdraw money from the account"""
    print_header("WITHDRAWAL MENU")
    global balance
    try:
        withdraw_amount = float(input("Enter amount to withdraw: $"))
        if withdraw_amount <= 0:
            print("\nWithdrawal amount must be greater than zero.")
        elif withdraw_amount > balance:
            print("\nInsufficient funds for withdrawal.")
        else:
            print(f"\nWithdraw ${withdraw_amount}")
            confirmation = input("Confirm Withdrawal (y/n): ").strip().lower()
            if confirmation == "y":
                balance -= withdraw_amount
                print(f"\nSuccessfully withdrew ${withdraw_amount}. New balance is: ${balance}")
                transaction_history.append(f"Withdrawal: -${withdraw_amount}")
            else:
                print("\nWithdrawal Cancelled by User.")
    except ValueError:
        print("\nInvalid input. Please enter a valid amount.")

transaction_history = []  # Placeholder for transaction history
def transactions():
    """Returns the transaction history"""
    print_header("TRANSACTION MENU")
    if len(transaction_history) == 0:
        print("\nNo transactions yet.")
    else:
        for transaction in transaction_history:
            print(transaction)

balance = 1000
while True:
    print_header("ATM SIMULATOR")
    
    show_menu()
    try:
        user_menu_option = int(input("\nEnter a menu option number (eg. 1 - 5): "))
        
        if user_menu_option not in range(1, 6):
            print("\nInvalid menu option. Please enter a number between 1 and 5.")
            time.sleep(1)
            continue
        
        if user_menu_option == 5:
            time.sleep(1)
            print("\nThank you for using our ATM.")
            clear_screen()
            break
        elif user_menu_option == 1:
            time.sleep(1)
            check_balance()
            pause_and_clear()
        elif user_menu_option == 2:
            time.sleep(1)
            deposit()
            pause_and_clear()
        elif user_menu_option == 3:
            time.sleep(1)
            withdraw()
            pause_and_clear()
        elif user_menu_option == 4:
            time.sleep(1)
            transactions()
            pause_and_clear()
        else:
            time.sleep(1)
            print("\nFeature coming soon...")
            clear_screen()
    except ValueError:
        print("\nInvalid input. Please enter a valid menu option number (eg. 1 - 5).")
        time.sleep(1)
        continue