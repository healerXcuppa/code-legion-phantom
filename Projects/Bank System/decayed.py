"""Bank System Program Version 1"""
# Importing the required modules
import secrets
import datetime
import time
import os
import shutil

width = shutil.get_terminal_size().columns

# Storing account numbers and account objects
existing_account_numbers = []
accounts = []

def delay():
    """Delay an operation"""
    time.sleep(1)

def clear_screen():
    """Clears the screen of the terminal"""
    os.system("cls" if os.name == "nt" else "clear")

def loading_screen(load_title):
    """Delay New Screen/Information"""
    print()
    input("Press any key to continue".center(width))
    print()
    print(load_title.center(width))
    delay()

def intro(intro_title):
    """Displays the intro of the bank system program"""
    delay()
    clear_screen()
    print("-" * width)
    print(intro_title.center(width))
    print("-" * width)
    delay()

def generate_account_number():
    """Returns the account number generated for each account object"""
    while True:
        obtained_secret_digits = []
        
        for _ in range(10):
            secret_digit = secrets.choice("0123456789")
            obtained_secret_digits.append(secret_digit)

        combined_secret_digit = "000"+"".join(obtained_secret_digits)
        
        if combined_secret_digit in existing_account_numbers:
            continue
        else:
            existing_account_numbers.append(combined_secret_digit)
            return combined_secret_digit

def generate_account_creation_date_and_time():
    """Returns the date and time of account creation for each account object"""
    current_date_and_time = datetime.datetime.now()
    formatted_date_and_time = current_date_and_time.strftime("%d %B %Y, %H:%M")
    return formatted_date_and_time

def find_account(account_number):
    """Returns the matching Account object or None."""
    for account in accounts:
        if account.get_account_number() == account_number:
            return account

def get_deposit():
    """Gets and validate the user deposit"""
    while True:
        try:
            amount = float(input("Enter your deposit amount: $"))
            
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            else:
                print(f"Successfully Deposited ${amount:.2f} to your account.")
                return amount
                
        except ValueError:
            print("Deposit amount must be numbers.")

def get_withdrawal():
    """Gets and validate the user withdrawal"""
    while True:
        try:
            amount = float(input("Enter your withdrawal amount: $"))
    
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            
            else:
                print(f"Cash Out ${amount:.2f} from your account.")
                return amount
    
        except ValueError:
            print("Withdrawal amount must be numbers.")

def get_transaction_info(transaction_type,transaction_amount):
    """Returns the date and time of when a transaction is completed"""
    current_date_and_time = datetime.datetime.now()
    formatted_date_and_time = current_date_and_time.strftime("%d %B %Y, %H:%M:%S")
    
    transaction = {
        "Transaction Type" : transaction_type,
        "Transaction Amount" : transaction_amount,
        "Transaction Time" : formatted_date_and_time
    }
    return transaction

def dashboard(account):
    """Display Account Dashboard Menu"""
    while True:
        print("ACCOUNT DASHBOARD LOADING...".center(width))
        intro("ACCOUNT DASHBOARD")
        dashboard_list = [
            "View Account Information",
            "Check Balance",
            "Deposit",
            "Withdraw",
            "Transaction History",
            "Log Out"
        ]
        
        print()
        for dashboard_index,dashboard_item in enumerate(dashboard_list):
            print(f"{dashboard_index + 1}. {dashboard_item}")

        try:
            dashboard_option = int(input("\nEnter a menu number: "))
            
            if dashboard_option not in range(1,7):
                print("\nEnter a valid menu option.")
                continue

            if dashboard_option == 6:
                print("Logging Out From Account...".center(width))
                delay()
                break
            elif dashboard_option == 1:
                intro("ACCOUNT INFORMATION")
                print()
                account_info(account)
                loading_screen("RETURNING TO DASHBOARD...")
                continue
            elif dashboard_option == 2:
                intro("ACCOUNT BALANCE")
                print()
                print(f"Account Name: {account.account_name}")
                print(f"Account Balance: ${account.get_account_balance():.2f}")
                loading_screen("RETURNING TO DASHBOARD")
                continue
            elif dashboard_option == 3:
                intro("DEPOSIT MENU")
                print()
                deposit_amount = get_deposit()
                deposit_transaction = get_transaction_info("Deposit",deposit_amount)
                account.add_transaction(deposit_transaction)
                new_balance = account.account_deposit(deposit_amount)
                print(f"\nAccount Balance : ${new_balance:.2f}")
                loading_screen("RETURNING TO DASHBOARD")
                continue
            elif dashboard_option == 4:
                intro("ACCOUNT WITHDRAWAL MENU")
                print()
                withdrawal_amount = get_withdrawal()
                withdrawal_retry = 0
                while True:
                    withdrawal_confirmation = input("\nDo you approve the transaction (y/n): ").lower()
                    if withdrawal_confirmation not in ("yes","y","no","n"):
                        withdrawal_retry +=1
                        print("Confirmation must be [yes(y)/no(n)]")
   
                    elif withdrawal_confirmation in ("no","n"):
                        print("\nWithdrawal Cancelled by user.")
                        break
                    else:
                        pin_retry = 0
                        while True:
                            if pin_retry == 3:
                                break

                            confirmation_pin = input("\nEnter your 4 digit transaction pin to continue: ").strip()

                            if not confirmation_pin.isdigit():
                                pin_retry += 1
                                print("Input must only be digits")    

                            elif len(confirmation_pin) != 4:
                                pin_retry += 1
                                print("Input must be 4 digits")

                            else:
                                confirmation_pin_result = account.verify_pin(confirmation_pin)

                                if confirmation_pin_result is True:
                                    withdrawal_status,balance_after_withdrawal = account.account_withdrawal(withdrawal_amount)
                                    if withdrawal_status:
                                        withdrawal_transaction = get_transaction_info("Withdrawal",withdrawal_amount)
                                        account.add_transaction(withdrawal_transaction)
                                        print("Transaction Successful".center(width))
                                        print(f"{'-'*10}".center(width))
                                        print(f"Current Balance: ${balance_after_withdrawal:.2f}".center(width))
                                        break
                                    else:
                                        print("Transaction Failed: Insufficient Balance".center(width))
                                        print(f"{'-'*10}".center(width))
                                        print(f"Account Balance: ${balance_after_withdrawal:.2f}".center(width))
                                        break
                                else:
                                    pin_retry += 1
                                    print("Pin Incorrect")

                        if confirmation_pin_result is True:
                            break
                        elif pin_retry == 3:
                            print("Pin retry limit reached")
                            break
                    if withdrawal_retry == 3:
                        print("Withdrawal retry limit reached")
                        break
                    else:
                        continue
                loading_screen("RETURNING TO DASHBOARD")
                continue
            if dashboard_option == 5:
                intro("TRANSACTION HISTORY")
                print()
                transactions = account.account_transaction_history()

                for transaction_index,transaction in enumerate(transactions):
                    print(f"\nTRANSACTION: {transaction_index + 1}:\n")
                    for key,value in transaction.items():
                        print(f"{key} : {value}")

                loading_screen("RETURNING TO DASHBOARD")
                continue
        except ValueError:
            print("Input must be a Menu Choice eg.(1 - 6)")
            continue

def account_info(account):
    """Displaying Safe Account Information"""
    print(f"Account Name: {account.account_name}")
    print(f"Account Number: {account.get_account_number()}")
    print(f"Account Email: {account.account_email}")
    print(f"Account Phone Number: {account.account_phone_number}")
    print(f"Account Type: {account.get_account_type()}")

class Account:
    """This is the Account class which builds each account of the bank system"""
    bank_name = "CODE LEGION BANK"
    #The init is responsible for determining what every account must contain
    def __init__(
        self,
        account_name,
        account_email,
        account_phone_number,
        account_password,
        account_pin,
        account_type,
        account_number,
        account_creation_date_and_time
    ):
        self.account_name = account_name
        self.account_email = account_email
        self.account_phone_number = account_phone_number
        self.__account_creation_date_and_time = account_creation_date_and_time
        self.__account_number = account_number
        self.__account_password = account_password
        self.__account_pin = account_pin
        self.__account_balance = 1000
        self._account_type = account_type
        self.__transaction_history = []

    def display_account_information(self):
        """Displays the account information of each account object"""
        print()
        print(f"Bank Name: {self.bank_name}")
        print(f"Account Name: {self.account_name}")
        print(f"Account Number: {self.__account_number}")
        print(f"Account Balance: ${self.__account_balance:.2f}")
        print(f"Account Type: {self._account_type}")
        print(f"Account Creation Date and Time: {self.__account_creation_date_and_time}")

    def get_account_number(self):
        """Returns the private account number"""
        return self.__account_number

    def verify_password(self,account_password):
        """Checks Password"""
        if account_password == self.__account_password:
            return True
        else:
            return False

    def get_account_balance(self):
        """Return Account Balance"""
        return self.__account_balance

    def get_account(self):
        """Returns account object pin"""
        return self.__account_pin

    def get_account_type(self):
        """Return account type"""
        return self._account_type

    def account_deposit(self,amount):
        """Deposit money into account"""
        self.__account_balance += amount
        return self.__account_balance

    def account_withdrawal(self,amount):
        """Withdraws money from account"""
        if amount > self.__account_balance:
            is_successful = False
            return is_successful,self.__account_balance
        else:
            is_successful = True
            self.__account_balance -= amount
            return is_successful,self.__account_balance

    def verify_pin(self,account_pin):
        """Verifies argument pin to account object pin"""
        if account_pin == self.__account_pin:
            return True
        else:
            return False

    def add_transaction(self,transaction):
        """Appends transaction to account transaction history"""
        self.__transaction_history.append(transaction)
        
    def account_transaction_history(self):
        """Returns the accoutnt transaction history"""
        return self.__transaction_history

def create_account():
    """Creates and stores a new bank account."""

    while True:
        intro("WELCOME TO CODE LEGION BANK")
        print("ACCOUNT REGISTRATION PORTAL".center(width))
        print("-"*width)
        account_type_list = ["Savings Account", "Current Account"]

        account_owner_name = input("\nEnter your full name: ").strip().upper()

        if not account_owner_name:
            print("Please input your full name.")
            continue

        while True:
            account_owner_email = input("\nEnter your email: ").strip()
            if not account_owner_email:
                continue
            elif account_owner_email[0] == "@":
                print("Email incorrect, check and retry")
                continue
            elif "@" not in account_owner_email or "." not in account_owner_email:
                print("Email incorrect, check and retry.")
                continue
            else:
                break

        while True:
            account_owner_phone_number = input("\nEnter your phone number: ").strip()

            # Checking that input is only numbers.
            if not account_owner_phone_number.isdigit():
                print("Phone number must contain digits only.")
                continue
            else:
                break
        
        while True:    
            account_owner_password = input("\nCreate a password for your account: ").strip()
            
            if len(account_owner_password) < 8:
                print("Use a strong password (8 characters or more)")
                continue
            elif account_owner_password.isdigit():
                print("Password must not be only numbers")
                continue
            elif account_owner_password.isalpha():
                print("Password must be alphanumeric.")
                continue
            else:
                break
        
        while True:
            account_owner_pin = input("\nCreate a 4 digit pin to approve account transactions: ").strip()
            
            if not account_owner_pin.isdigit():
                print("Pin must be 4 digits")
                continue
            elif len(account_owner_pin) != 4:
                print("Pin must be 4 digits")
            else:
                break
 
        while True:
            for index,account_selection in enumerate(account_type_list):
                print(f"{index + 1}. {account_selection}")
            
            try:
                account_owner_type = int(input("\nEnter account selection option (eg. 1 or 2): "))
                if account_owner_type not in range(1,3):
                    print("Input must be a menu number")
                    continue
                elif account_owner_type ==1:
                    account_owner_type = account_type_list[0]
                    break
                elif account_owner_type ==2:
                    account_owner_type = account_type_list[1]
                    break
            except ValueError:
                print("Input must be an integer")

        generated_account_number = generate_account_number()
        generated_account_creation_date_and_time = generate_account_creation_date_and_time()
        
        account1 = Account(
            account_name = account_owner_name,
            account_email = account_owner_email,
            account_phone_number = account_owner_phone_number,
            account_password = account_owner_password,
            account_pin = account_owner_pin,
            account_type = account_owner_type,
            account_number = generated_account_number,
            account_creation_date_and_time = generated_account_creation_date_and_time
        )
        
        accounts.append(account1)
        loading_screen("GENERATING CREATED ACCOUNT DATA...")
        intro("ACCOUNT CREATED SUCCESSFULLY")
        account1.display_account_information()
        break

create_account()
while True:
    loading_screen("ACCOUNT LOGIN PAGE LOADING...")
    intro("ACCOUNT LOGIN PAGE")
    
    search_account_number = input("\nEnter Account Number: ").strip()
    
    if not search_account_number.isdigit():
        print("\nAccount number must be only digits.")
        delay()
        continue
    elif len(search_account_number) != 13:
        print("\nAccount Number must be 13 digit.")
        delay()
        continue
    else:
        result = find_account(search_account_number)
        
        if result is None:
            print(f"\nAccount with Account Number: {search_account_number} Not Found.")
            delay()
            continue
        else:
            print("\nAccount Found:")
            print(f"Account Name: {result.account_name}")
            
            password_retry_count = 0
            while True:
                password_verification = input("\nEnter account password: ").strip()
                password_result = result.verify_password(password_verification)
                
                if password_result is True:
                    print(f"Account Name: {result.account_name}".center(width)) 
                    print(f"Account Number: {result.get_account_number()}".center(width)) 
                    print()
                    print("ACCOUNT CREDENTALS MATCHED.".center(width))
                    delay()
                    break
                else:
                    password_retry_count += 1
                    print("Password Incorrect, Check password and retry.")
                    
                if password_retry_count == 3:
                    print("Maximum Password Attempts Reached.")
                    break
            dashboard(result)