import os
import sys
import time
import shutil
from datetime import datetime
import database as db
import authentication as auth
import banking_operations as ops
import utilities as util
import customer as cust
import account as acc
import session as sess

global_width = shutil.get_terminal_size().columns

def clear_screen():
    """Clears the screen of the terminal"""
    os.system("cls" if os.name == "nt" else "clear")

def sleep():
    """Delays an operation using the sleep method"""
    time.sleep(1.5)

def main_banner():
    """Displays main menu banner for the bank"""
    clear_screen()

    # Get the width of the terminal for formatting
    width = global_width

    print("-" * width)
    print("C O D E   L E G I O N   B A N K".center(width))
    print("Secure Terminal System".center(width))
    print("-" * width)
    print()

def sub_menu(menu_title):
    """Displays the sub menu banners for the bank"""
    clear_screen()

    # Get the width of the terminal for formatting
    width = global_width

    print("-"*width)
    print(f"[ CODE LEGION BANK :: {menu_title.upper()} ]".center(width))
    print("-"*width)
    print("")

def loading_screen(message,delay=1.5):
    """Creates a smooth loading animation in the terminal."""
    print(f"\n{message}", end="", flush=True)
    for _ in range(3):
        time.sleep(delay / 3)
        print(".", end="", flush=True)
    print("\n")

# ==============================================================================
# ACCOUNT OPERATIONS MENU WORKFLOW (LEVEL 3)
# ==============================================================================
def account_operations_workflow(session):
    """Handles financial operations for the currently active account session"""

    while True:
        # Retrieve active customer and account objects from session
        active_customer = session.get_current_customer()
        active_account = session.get_current_account()

        # Calculate display balance in GHC
        current_balance_ghc = active_account.get_account_balance() / 100.0

        # --- ACCOUNT OPERATIONS HEADER BANNER ---
        clear_screen()
        print("=" * global_width)
        print(f"[ACCOUNT OWNER: {active_customer.get_customer_name()}]".center(global_width))
        print(f" ACTIVE ACCOUNT: #{active_account.get_account_number()} ({active_account.get_account_type()}) ".center(global_width))
        print(f" Current Balance: GHC {current_balance_ghc:,.2f} ".center(global_width))
        print("=" * global_width)
        print()

        # List of available account operations
        account_options = [
            "Deposit Funds",
            "Withdraw Funds",
            "Transfer Funds",
            "View Transaction History",
            "Return to Customer Menu"
        ]

        # Enumerate and display account operations
        for idx, option in enumerate(account_options, start=1):
            print(f"[{idx}]. {option}")
        print()

        try:
            choice = int(input("Select account operation (1-5): "))

            if choice == 1:
                deposit_workflow(active_account)
                sleep()

            elif choice == 2:
                withdraw_workflow(active_account)
                sleep()

            elif choice == 3:
                transfer_workflow(active_account)
                sleep()

            elif choice == 4:
                transaction_history_workflow(active_account)
                sleep()

            elif choice == 5:
                # Return from account operations back to customer dashboard
                loading_screen("Returning to Customer Menu")
                break

            else:
                print("Invalid option! Please select between 1 and 5.")
                sleep()

        except ValueError:
            print("Input must be a valid number.")
            sleep()

# ==============================================================================
# CUSTOMER DASHBOARD WORKFLOW (LEVEL 2)
# ==============================================================================
def customer_dashboard_workflow(session, customer):
    """Displays the customer level dashboard for account management and profile edits"""

    while True:
        loading_screen("Opening Customer Menu")
        sub_menu(f"CUSTOMER MENU :: {customer.get_customer_name()}")

        # Customer Dashboard Options
        menu_list = [
            "View / Select Active Bank Account",
            "Create New Bank Account",
            "Change Email Address",
            "Change Phone Number",
            "Logout Customer Session"
        ]

        # Enumerate menu options for display
        for menu_index, menu_item in enumerate(menu_list, start=1):
            print(f"[{menu_index}]. {menu_item}")
        print()

        try:
            menu_choice = int(input("Enter a menu option (1-5): "))

            if menu_choice not in range(1, 6):
                print("Invalid choice! Enter a number between 1 and 5.")
                sleep()
                continue

            # ------------------------------------------------------------------
            # OPTION 1: VIEW & SELECT ACTIVE BANK ACCOUNT
            # ------------------------------------------------------------------
            if menu_choice == 1:
                loading_screen("Loading customer accounts")
                sub_menu(f"{customer.get_customer_name()}'s Accounts")

                # Takes the authenticated customer from the login session and find customer accounts
                active_customer_id = customer.get_customer_id()
                accounts = db.get_customer_accounts(active_customer_id)

                # Checks for no accounts found under authenticated customer
                if not accounts:
                    print("No active bank accounts found under your customer profile.")
                    print("Please choose Option 2 to create a new account.")
                    sleep()
                    loading_screen("Going back to customer menu")
                    continue

                selected_account = None

                # Automatically select if only one account exists
                if len(accounts) == 1:
                    selected_account = accounts[0]
                else:
                    print("Select an Account for this session:\n")
                    for idx, acc_obj in enumerate(accounts, start=1):
                        print(f"[{idx}]. Account Label: {acc_obj.get_account_label()} (#{acc_obj.get_account_number()})")

                    acc_choice_retry = 3
                    while acc_choice_retry > 0:
                        try:
                            acc_choice = int(input("\nSelect account option number: "))

                            # Checks user input to list index for selection
                            if 1 <= acc_choice <= len(accounts):
                                selected_account = accounts[acc_choice - 1]
                                break
                            else:
                                acc_choice_retry -= 1
                                print(f"Please select a valid option (1 - {len(accounts)}).")
                                sleep()
                        except ValueError:
                            print("Input must be a valid number.")
                            sleep()

                    if selected_account is None:
                        print("Failed many attepts to select an account choice")
                        loading_screen("Returning to customer menu")
                        continue

                # Bind selected active account to current user session
                loading_screen("Binding account session")
                session.set_active_account(selected_account)

                # Enter Level 3: Account Operations Menu
                account_operations_workflow(session)

            # ------------------------------------------------------------------
            # OPTION 2: CREATE NEW BANK ACCOUNT
            # ------------------------------------------------------------------
            elif menu_choice == 2:
                create_account_workflow(customer)

            # ------------------------------------------------------------------
            # OPTION 3: CHANGE EMAIL ADDRESS
            # ------------------------------------------------------------------
            elif menu_choice == 3:
                change_email_workflow(customer)

            # ------------------------------------------------------------------
            # OPTION 4: CHANGE PHONE NUMBER
            # ------------------------------------------------------------------
            elif menu_choice == 4:
                change_phone_workflow(customer)

            # ------------------------------------------------------------------
            # OPTION 5: LOGOUT SESSION
            # ------------------------------------------------------------------
            elif menu_choice == 5:
                loading_screen("Logging out customer session")
                session.clear_session()
                print("Successfully logged out.")
                sleep()
                break  # Exit Customer Dashboard loop back to Unauthenticated Main Menu

        except ValueError:
            print("Please enter a valid menu number (1 - 5).")
            sleep()

# ==============================================================================
# AUTHENTICATION WORKFLOW (LEVEL 1)
# ==============================================================================
def login_customer_workflow(session):
    """Authenticate an existing customer and launch customer dashboard session"""

    sub_menu("CUSTOMER LOGIN")

    id_attempts = 3
    customer = None

    # STAGE 1: CUSTOMER ID VALIDATION & DB LOOKUP
    while id_attempts > 0:
        customer_id = input("Enter your Customer ID (e.g., CUST-XXXXX): ").strip().upper()

        if not customer_id:
            id_attempts -= 1
            print("Customer ID cannot be empty.")
            print(f"Attempts remaining: {id_attempts}")
            sleep()
            sub_menu("CUSTOMER LOGIN")
            continue

        # Look up customer record in database
        customer = db.find_customer(customer_id)

        if not customer:
            id_attempts -= 1
            print(f"No profile found matching Customer ID '{customer_id}'.")
            print(f"Attempts remaining: {id_attempts}")
            sleep()
            sub_menu("CUSTOMER LOGIN")
            continue

        # Breaks loop when a valid stored customer id is provided
        break

    if not customer:
        print("\nToo many failed Customer ID attempts. Returning to main menu.")
        sleep()
        return

    # STAGE 2: PASSWORD AUTHENTICATION
    password_attempts = 3
    is_authenticated = False

    while password_attempts > 0:
        password = input(f"Enter Password for [{customer.get_customer_name()}]: ").strip()

        # Checks no data input for password
        if not password:
            password_attempts -= 1
            print("No password input detected, check and retry.")
            print(f"Attempts remaining: {password_attempts}")
            sleep()
            continue

        if not auth.verify_password(customer.get_customer_password_hash(), password):
            password_attempts -= 1
            print("Invalid password!")
            print(f"Attempts remaining: {password_attempts}")
            sleep()
            continue

        is_authenticated = True
        break

    if not is_authenticated:
        print("\nToo many failed password attempts. Access denied.")
        sleep()
        return

    # Start customer level session state
    session.start_session(customer)

    # Launch Customer Dashboard loop (Level 2)
    customer_dashboard_workflow(session, customer)

# ==============================================================================
# REGISTRATION WORKFLOW (LEVEL 0)
# ==============================================================================
def register_customer_workflow():
    """Create and Save new customer to bank database"""

    sub_menu("REGISTER NEW CUSTOMER")
    print("Please fill in your details to create a new customer profile.\n")

    # 1. Full Name Input & Validation
    while True:
        name = input("Enter your full name: ").strip().upper()
        if not name:
            print("Name cannot be empty. Please enter your name.")
            sleep()
        elif any(char.isdigit() for char in name):
            print("Name cannot contain numbers. Please enter a valid real name.")
            sleep()
        else:
            break

    # 2. Email Address Input & Validation
    while True:
        email = input("Enter your email address: ").strip().lower()
        if not email:
            print("Email cannot be empty.")
            sleep()
        elif email.startswith("@") or "@" not in email or "." not in email:
            print("Invalid email format! Example: user@example.com")
            sleep()
        else:
            break

    # 3. Phone Number Input & Validation
    while True:
        phone_number = input("Enter your phone number: ").strip()
        if not phone_number.isdigit():
            print("Phone number must contain digits only.")
            sleep()
        elif not 8 <= len(phone_number) <= 15:
            print("Phone number length must be between 8 and 15 digits.")
            sleep()
        else:
            break

    # 4. Date of Birth Input & Validation (YYYY-MM-DD)
    while True:
        dob_input = input("Enter date of birth (YYYY-MM-DD): ").strip()
        try:
            valid_dob = datetime.strptime(dob_input, "%Y-%m-%d").date()
            date_of_birth = str(valid_dob)
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD (e.g., 2005-08-25).")
            sleep()

    # 5. Customer Password Input & Hashing
    while True:
        password = input("Create a password (min 8 characters): ").strip()
        if len(password) < 8:
            print("Password must be at least 8 characters long.")
            sleep()
        else:
            confirm_password = input("Confirm your password: ").strip()
            if password != confirm_password:
                print("Passwords do not match! Please try again.")
                sleep()
            else:
                break

    # 6. Generate Unique Customer ID and Hash Password
    customer_id = util.generate_customer_id()
    hashed_password = auth.hash_password(password)

    # 7. Creating Customer Object
    new_customer = cust.Customer(
        customer_id=customer_id,
        customer_name=name,
        customer_email=email,
        customer_phone_num=phone_number,
        customer_date_of_birth=date_of_birth,
        customer_password_hash=hashed_password
    )

    # 8. Save Customer Profile to Database
    db.save_customer(new_customer)

    # 9. Display Success Feedback & New Customer ID
    loading_screen("Finalizing customer profile creation")
    clear_screen()
    print("=" * global_width)
    print(f" SUCCESS! Profile created successfully for {name}.".center(global_width))
    print(f" YOUR CUSTOMER ID IS: {customer_id}".center(global_width))
    print(" Please keep this Customer ID safe — you will need it to login!".center(global_width))
    print("=" * global_width)
    print("\nPress ENTER to return to the main menu...", end="")
    input()

# ==============================================================================
# ACCOUNT CREATION WORKFLOW (lEVEL 2 - SUB 1)
# ==============================================================================
def create_account_workflow(customer):
    """Workflow to create and save a new bank account to an active customer"""

    sub_menu("CREATE NEW BANK ACCOUNT")
    print(f"Creating a new bank account profile for: {customer.get_customer_name()}\n")

    # --------------------------------------------------------------------------
    # 1. ACCOUNT TYPE SELECTION LOOP
    # --------------------------------------------------------------------------
    account_types = ["Savings Account", "Current Account"]
    selected_account_type = None

    while True:
        print("Select Account Type:")
        for index,acc_type in enumerate(account_types,start=1):
            print(f"[{index}]. {acc_type}")

        try:
            type_choice = int(input("\nEnter choice (1-2): "))

            # Validate account type choice
            if type_choice in [1, 2]:
                selected_account_type = account_types[type_choice - 1]
                break
            else:
                print("Invalid choice! Please select 1 for Savings or 2 for Current.")
                sleep()
                sub_menu("CREATE NEW BANK ACCOUNT")

        except ValueError:
            # Handle non-numeric choice input
            print("Input must be a valid number (1 or 2).")
            sleep()
            sub_menu("CREATE NEW BANK ACCOUNT")

    # --------------------------------------------------------------------------
    # 2. ACCOUNT LABEL / NICKNAME INPUT & VALIDATION LOOP
    # --------------------------------------------------------------------------
    while True:
        acc_nick = input("\nEnter a custom account label (e.g., School Funds ): ").strip().title()

        # Check if account label input is empty
        if not acc_nick:
            print("Account label cannot be empty. Please enter a identifier.")
            sleep()
            continue

        # Check for maximum character length on account label
        if len(acc_nick) > 30:
            print("Account label must be 30 characters or fewer.")
            sleep()
            continue

        break

    # --------------------------------------------------------------------------
    # 3. INITIAL DEPOSIT AMOUNT VALIDATION (PESEWA CONVERSION)
    # --------------------------------------------------------------------------
    initial_amount = 0

    while True:
        try:
            initial_deposit = float(input("\nEnter initial deposit amount (GHC): "))

            # Check for invalid amount deposit
            if initial_deposit <= 0:
                print("Initial deposit must be higher than (GHC 0.00)")
                sleep()
                continue

            # Convert GHC amount to integer pesewas (1 GHC = 100 pesewas)
            initial_amount = int(round(initial_deposit,2)*100)
            break

        except ValueError:
            print("Invalid currency value! Enter a valid amount.")
            sleep()

    # --------------------------------------------------------------------------
    # 4. ACCOUNT 4-DIGIT PIN SETUP & CONFIRMATION LOOP
    # --------------------------------------------------------------------------
    hashed_pin = None

    while True:
        pin = input("\nCreate a 4-digit Account PIN: ").strip()

        # Check if PIN contains non-digit characters
        if not pin.isdigit():
            print("Account PIN must contain numeric digits only!")
            sleep()
            continue

        # Check for exact 4-digit PIN length
        if len(pin) != 4:
            print("Account PIN must be exactly 4 digits long!")
            sleep()
            continue

        # Prompt for PIN confirmation
        confirm_pin = input("Confirm your 4-digit Account PIN: ").strip()

        # Verify matching PIN entries
        if pin != confirm_pin:
            print("PIN entries do not match! Please try again.")
            sleep()
            continue

        # Hash the 4-digit PIN for database storage
        hashed_pin = auth.hash_pin(pin)
        # Break out of PIN setup loop
        break

    # --------------------------------------------------------------------------
    # 5. INSTANTIATION, DB PERSISTENCE & BANKING OPERATIONS DEPOSIT
    # --------------------------------------------------------------------------
    generated_account_number = util.generate_account_number()

    account_created = acc.Account(
        account_number = generated_account_number,
        account_label = acc_nick,
        account_type = selected_account_type,
        account_balance = 0,
        account_pin_hash = hashed_pin,
        account_customer_id = customer.get_customer_id(),
        account_creation_date = util.generate_timestamp()
    )


    # Save new account record to database
    db.save_account(account_created)

    # Process initial deposit using banking_operations
    deposit = ops.deposit(account_created.get_account_number(), initial_amount)
    account_created.deposit(initial_amount)

    # --------------------------------------------------------------------------
    # 6. DISPLAY SUCCESS BANNER (FORMATTED CURRENCY)
    # --------------------------------------------------------------------------
    if deposit:
        loading_screen("Finalizing new bank account creation")
        clear_screen()
        print("=" * global_width)
        print(" SUCCESS! NEW BANK ACCOUNT OPENED ".center(global_width))
        print(f" Account Number : {generated_account_number} ".center(global_width))
        print(f" Account Label  : {acc_nick} ".center(global_width))
        print(f" Account Type   : {selected_account_type} ".center(global_width))
        print(f" Opening Balance: GHC {account_created.get_account_balance()/100:,.2f} ".center(global_width))
        print("=" * global_width)
        print("\nPress ENTER to return to the Customer Menu...", end="")
        input()
    else:
        loading_screen("Finalizing new bank account creation")
        clear_screen()
        print("=" * global_width)
        print(" SUCCESS! NEW BANK ACCOUNT OPENED ".center(global_width))
        print(f" Account Number : {generated_account_number} ".center(global_width))
        print(f" Account Label  : {acc_nick} ".center(global_width))
        print(f" Account Type   : {selected_account_type} ".center(global_width))
        print(" Opening Balance: Initial Deposit Failed".center(global_width))
        print("=" * global_width)
        print("\nPress ENTER to return to the Customer Menu...", end="")
        input()

# ==============================================================================
# CHANGE EMAIL WORKFLOW (LEVEL 2 - SUB 2)
# ==============================================================================
def change_email_workflow(customer):
    """Workflow to update customer's email address in database and session memory"""

    sub_menu("CHANGE EMAIL ADDRESS")
    current_email = customer.get_customer_email()
    print(f"Current Email Address: {current_email}\n")

    # --------------------------------------------------------------------------
    # 1. NEW EMAIL INPUT & VALIDATION LOOP
    # --------------------------------------------------------------------------
    while True:
        new_email = input("Enter new email address: ").strip().lower()

        # Check for empty string input
        if not new_email:
            print("Email cannot be empty. Please enter a valid email.")
            sleep()
            continue

        # Format verification checks
        if new_email.startswith("@") or "@" not in new_email or "." not in new_email:
            print("Invalid email format! Example: user@example.com")
            sleep()
            continue

        # Check if new email matches current registered email
        if new_email == current_email:
            print("New email cannot be identical to your current email address.")
            sleep()
            continue

        break

    # --------------------------------------------------------------------------
    # 2. PERSIST TO DATABASE & UPDATE MEMORY OBJECT
    # --------------------------------------------------------------------------
    customer_id = customer.get_customer_id()

    # Execute database update query helper
    db.update_customer_email(customer_id, new_email)

    # Update in-memory customer instance state
    customer.change_email(new_email)

    # --------------------------------------------------------------------------
    # 3. DISPLAY SUCCESS FEEDBACK BANNER
    # --------------------------------------------------------------------------
    loading_screen("Updating email record in database")
    clear_screen()
    print("=" * global_width)
    print(" SUCCESS! EMAIL ADDRESS UPDATED ".center(global_width))
    print(f" New Email: {new_email} ".center(global_width))
    print("=" * global_width)
    print("\nPress ENTER to return to the Customer Menu...", end="")
    input()

# ==============================================================================
# CHANGE PHONE NUMBER WORKFLOW (LEVEL 2 - SUB 3)
# ==============================================================================
def change_phone_workflow(customer):
    """Workflow to update customer's phone number in database and session memory"""

    sub_menu("CHANGE PHONE NUMBER")
    current_phone = customer.get_customer_phone_num()
    print(f"Current Phone Number: {current_phone}\n")

    # --------------------------------------------------------------------------
    # 1. NEW PHONE NUMBER INPUT & VALIDATION LOOP
    # --------------------------------------------------------------------------
    while True:
        new_phone = input("Enter new phone number: ").strip()

        # Check for non-digit characters
        if not new_phone.isdigit():
            print("Phone number must contain numeric digits only.")
            sleep()
            continue

        # Validate allowed length range
        if not 8 <= len(new_phone) <= 15:
            print("Phone number length must be between 8 and 15 digits.")
            sleep()
            continue

        # Check if new phone number matches current registered phone
        if new_phone == current_phone:
            print("New phone number cannot be identical to your current number.")
            sleep()
            continue

        break

    # --------------------------------------------------------------------------
    # 2. PERSIST TO DATABASE & UPDATE MEMORY OBJECT
    # --------------------------------------------------------------------------
    customer_id = customer.get_customer_id()

    # Execute database update query helper
    db.update_customer_phone(customer_id,new_phone)

    # Update in-memory customer instance state
    customer.change_phone(new_phone)

    # --------------------------------------------------------------------------
    # 3. DISPLAY SUCCESS FEEDBACK BANNER
    # --------------------------------------------------------------------------
    loading_screen("Updating phone record in database")
    clear_screen()
    print("=" * global_width)
    print(" SUCCESS! PHONE NUMBER UPDATED ".center(global_width))
    print(f" New Phone: {new_phone} ".center(global_width))
    print("=" * global_width)
    print("\nPress ENTER to return to the Customer Menu...", end="")
    input()

# ==============================================================================
# DEPOSIT WORKFLOW (LEVEL 3 - SUB 1)
# ==============================================================================
def deposit_workflow(active_account):
    """Workflow to deposit funds into the active bank account"""

    sub_menu("DEPOSIT FUNDS")
    current_balance = active_account.get_account_balance() / 100
    print(f"Active Account: #{active_account.get_account_number()} ({active_account.get_account_label()})")
    print(f"Current Balance: GHC {current_balance:,.2f}")

    # --------------------------------------------------------------------------
    # 1. DEPOSIT AMOUNT INPUT & VALIDATION LOOP
    # --------------------------------------------------------------------------
    deposit_amount = 0

    while True:
        try:
            deposit_input = float(input("\nEnter deposit amount (GHC): "))

            # Check for non-positive deposit amount error
            if deposit_input <= 0:
                print("Deposit amount must be greater than GHC 0.00!")
                sleep()
                continue

            # Convert GHC amount to integer pesewas (1 GHC = 100 pesewas)
            deposit_amount = int(round(deposit_input, 2) * 100)
            break

        except ValueError:
            print("\nInvalid currency value! Enter a valid decimal amount (e.g., 50.00).")
            sleep()

    # --------------------------------------------------------------------------
    # 2. EXECUTE BANKING OPERATION & LOG TRANSACTION
    # --------------------------------------------------------------------------
    loading_screen("Processing cash deposit")

    # Execute deposit through operations module (updates DB and active_account object)
    ops.deposit(active_account.get_account_number(), deposit_amount)

    # Updating the account balance in memory
    active_account.deposit(deposit_amount)
    new_balance = (active_account.get_account_balance()) / 100.0

    # --------------------------------------------------------------------------
    # 3. DISPLAY SUCCESS FEEDBACK BANNER
    # --------------------------------------------------------------------------
    clear_screen()
    print("=" * global_width)
    print(" DEPOSIT SUCCESSFUL ".center(global_width))
    print(f" Account Number : #{active_account.get_account_number()} ".center(global_width))
    print(f" Deposited      : GHC {deposit_amount / 100:,.2f} ".center(global_width))
    print(f" New Balance    : GHC {new_balance:,.2f} ".center(global_width))
    print("=" * global_width)
    print("\nPress ENTER to return to Account Operations...", end="")
    input()

# ==============================================================================
# WITHDRAW WORKFLOW (LEVEL 3 - SUB 2)
# ==============================================================================
def withdraw_workflow(active_account):
    """Workflow to withdraw funds from the active bank account after PIN check"""

    sub_menu("WITHDRAW FUNDS")
    current_balance = active_account.get_account_balance()
    current_balance_ghc = current_balance / 100

    print(f"Active Account: #{active_account.get_account_number()} ({active_account.get_account_label()})")
    print(f"Current Balance: GHC {current_balance_ghc:,.2f}")

    # --------------------------------------------------------------------------
    # 2. WITHDRAWAL AMOUNT INPUT & BALANCE VALIDATION LOOP
    # --------------------------------------------------------------------------
    withdraw_amount = 0

    while True:
        try:
            withdraw_input = float(input("\nEnter withdrawal amount (GHC): "))

            # Check for non-positive withdrawal amount error
            if withdraw_input <= 0:
                print("Withdrawal amount must be greater than GHC 0.00!")
                sleep()
                continue

            # Convert GHC amount to integer pesewas
            withdraw_amount = int(round(withdraw_input, 2) * 100)

            # Validate sufficient funds balance check
            if withdraw_amount > current_balance:
                print(f"Insufficient funds! Maximum available: GHC {current_balance_ghc:,.2f}")
                sleep()
                continue

            break

        except ValueError:
            print("\nInvalid currency value! Enter a valid decimal amount (e.g., 20.00).")
            sleep()

    # --------------------------------------------------------------------------
    # 1. 4-DIGIT ACCOUNT PIN SECURITY VERIFICATION LOOP
    # --------------------------------------------------------------------------
    pin_attempts = 3
    is_pin_verified = False

    while pin_attempts > 0:
        pin_input = input("\nEnter 4-digit Account PIN: ").strip()

        # Check for empty input
        if not pin_input:
            print("PIN cannot be empty.")
            pin_attempts -= 1
            print(f"Attempts remaining: {pin_attempts}")
            sleep()
            continue

        # Verify input PIN against stored account PIN hash
        if not auth.verify_pin(active_account.get_account_pin_hash(), pin_input):
            print("Invalid Account PIN!")
            pin_attempts -= 1
            print(f"Attempts remaining: {pin_attempts}")
            sleep()
            continue

        is_pin_verified = True
        break

    if not is_pin_verified:
        print("\nToo many failed PIN attempts. Withdrawal canceled.")
        sleep()
        return

    # --------------------------------------------------------------------------
    # 3. EXECUTE BANKING OPERATION & LOG TRANSACTION
    # --------------------------------------------------------------------------
    loading_screen("Dispensing cash withdrawal")

    # Execute withdrawal through operations module
    ops.withdraw(active_account.get_account_number(), withdraw_amount)

    # Update the new balance in memory
    active_account.withdraw(withdraw_amount)
    new_balance_ghc = (active_account.get_account_balance()) / 100

    # --------------------------------------------------------------------------
    # 4. DISPLAY SUCCESS FEEDBACK BANNER
    # --------------------------------------------------------------------------
    clear_screen()
    print("=" * global_width)
    print(" WITHDRAWAL SUCCESSFUL ".center(global_width))
    print(f" Account Number : #{active_account.get_account_number()} ".center(global_width))
    print(f" Withdrawn      : GHC {withdraw_amount / 100:,.2f} ".center(global_width))
    print(f" Remaining Bal  : GHC {new_balance_ghc:,.2f} ".center(global_width))
    print("=" * global_width)
    print("\nPress ENTER to return to Account Operations...", end="")
    input()

# ==============================================================================
# TRANSFER WORKFLOW (LEVEL 3 - SUB 3)
# ==============================================================================
def transfer_workflow(active_account):
    """Workflow to transfer funds from active account to another bank account"""

    sub_menu("TRANSFER FUNDS")
    sender_balance_amount = active_account.get_account_balance()
    sender_balance_ghc = sender_balance_amount / 100

    print(f"Sender Account: #{active_account.get_account_number()} ({active_account.get_account_label()})")
    print(f"Available Balance: GHC {sender_balance_ghc:,.2f}")

    # --------------------------------------------------------------------------
    # 1. RECIPIENT ACCOUNT LOOKUP & VALIDATION
    # --------------------------------------------------------------------------
    recipient_account = None

    while True:
        recipient_acc_num = input("\nEnter Recipient Account Number: ").strip()

        # Check for empty input
        if not recipient_acc_num:
            print("Recipient account number cannot be empty.")
            sleep()
            continue

        # Prevent transferring funds to self
        if recipient_acc_num == active_account.get_account_number():
            print("You cannot transfer funds to the same active account!")
            sleep()
            continue

        # Query database for recipient account object
        recipient_account = db.find_account(recipient_acc_num)

        # Handle account lookup failure
        if not recipient_account:
            print(f"No bank account found matching Account Number '{recipient_acc_num}'.")
            sleep()
            continue

        # Assessing recipient customer details based on the recipient customer id
        else:
            recipient_customer = db.find_customer(recipient_account.get_account_customer_id())

        break

    print(f"Recipient Found: {recipient_customer.get_customer_name()} : (#{recipient_account.get_account_number()})\n")

    # --------------------------------------------------------------------------
    # 2. TRANSFER AMOUNT INPUT & BALANCE VALIDATION LOOP
    # --------------------------------------------------------------------------
    transfer_amount = 0

    while True:
        try:
            transfer_input = float(input("\nEnter transfer amount (GHC): "))

            if transfer_input <= 0:
                print("Transfer amount must be greater than GHC 0.00!")
                sleep()
                continue

            # Convert GHC amount to integer pesewas
            transfer_amount = int(round(transfer_input, 2) * 100)

            # Validate sender has sufficient funds
            if transfer_amount > sender_balance_amount:
                print(f"Insufficient balance! Available: GHC {sender_balance_ghc:,.2f}")
                sleep()
                continue
            break

        except ValueError:
            print("Invalid currency value! Enter a valid decimal amount (e.g., 100.00).")
            sleep()

    # --------------------------------------------------------------------------
    # 3. TRANSFER CONFIRMATION AND ACCOUNT PIN SECURITY VERIFICATION
    # --------------------------------------------------------------------------

    # Get confirmation for transaction based on the recipient customer name
    try:
        confirm_list = ["yes","no"]

        print("\nSelect 1 to proceed or 2 to cancel transfer: ")
        for index,confirm_value in enumerate(confirm_list):
            print(f"[{index + 1}]. {confirm_value}")

        confirmation = int(input("\nDo you approve of the confirmation: "))

        if confirmation not in range(1,3):
            print("Transfer cofirmation failed.")
            sleep()
            return

        if confirmation == 2:
            print("Transfer cancelled by user")
            sleep()
            return
    except ValueError:
        print("Error during transafer confirmation")
        sleep()
        return

    # PIN AUTHOURIZATION
    pin_attempts = 3
    is_pin_verified = False
    while pin_attempts > 0:
        pin_input = input("\nEnter your 4-digit Account PIN to authorize: ").strip()

        # Check for empty pin inputs
        if not pin_input:
            print("PIN cannot be empty.")
            pin_attempts -= 1
            print(f"Attempts remaining: {pin_attempts}")
            sleep()
            continue

        # Verify PIN against active sender account pin hash
        if not auth.verify_pin(active_account.get_account_pin_hash(), pin_input):
            print("Invalid Account PIN!")
            pin_attempts -= 1
            print(f"Attempts remaining: {pin_attempts}")
            sleep()
            continue

        is_pin_verified = True
        break

    if not is_pin_verified:
        print("\nToo many failed PIN attempts. Transfer authorization canceled.")
        sleep()
        return

    # --------------------------------------------------------------------------
    # 4. EXECUTE ATOMIC TRANSFER OPERATION & LOG TRANSACTIONS
    # --------------------------------------------------------------------------
    loading_screen("Executing fund transfer")

    # Perform atomic transfer across sender and recipient account objects
    ops.transfer(active_account.get_account_number(), recipient_account.get_account_number(), transfer_amount)

    # UPDATING IN MEMORY ACCOUNT BALANCE
    active_account.withdraw(transfer_amount)
    new_sender_balance_ghc = (active_account.get_account_balance()) / 100.0

    # --------------------------------------------------------------------------
    # 5. DISPLAY SUCCESS FEEDBACK BANNER
    # --------------------------------------------------------------------------
    clear_screen()
    print("=" * global_width)
    print(" TRANSFER SUCCESSFUL ".center(global_width))
    print(f" From Account : #{active_account.get_account_number()} ".center(global_width))
    print(f" To Account   : #{recipient_account.get_account_number()} ".center(global_width))
    print(f" Amount       : GHC {transfer_amount / 100:,.2f} ".center(global_width))
    print(f" New Balance  : GHC {new_sender_balance_ghc:,.2f} ".center(global_width))
    print("=" * global_width)
    print("\nPress ENTER to return to Account Operations...", end="")
    input()

# ==============================================================================
# TRANSACTION HISTORY WORKFLOW (LEVEL 3 - SUB 4)
# ==============================================================================
def transaction_history_workflow(active_account):
    """Workflow to display formatted transaction logs for the active bank account"""

    sub_menu("TRANSACTION HISTORY")
    account_number = active_account.get_account_number()
    print(f"Displaying ledger history for Account: #{account_number} ({active_account.get_account_label()})\n")

    # --------------------------------------------------------------------------
    # 1. FETCH TRANSACTION LOGS FROM DATABASE
    # --------------------------------------------------------------------------
    logs = db.get_transaction(account_number)

    # Check if transaction history is empty
    if not logs:
        print("No transactions recorded for this account yet.")
        print("\nPress ENTER to return to Account Operations...", end="")
        input()
        return

    # --------------------------------------------------------------------------
    # 2. DISPLAY FORMATTED TRANSACTION TABLE
    # --------------------------------------------------------------------------

    # Making examplary table head in terminal
    print(f"{'TX ID':<10} | {'DATE & TIME':<20} | {'TYPE':<12} | {'AMOUNT (GHC)':<14} | {'BALANCE AFTER':<14}")
    print("-" * global_width)

    # Since logs contains a list of transactions
    for record in logs:
        tx_id = record.get_transaction_id()
        tx_type = record.get_transaction_type()
        tx_amount_ghc = record.get_transaction_amount()
        bal_after_ghc = record.get_balance_after()
        tx_date = record.get_transaction_timestamp()

        # Print formatted row using string column widths for tabular alignment
        print(f"{tx_id:<10} | {tx_date:<20} | {tx_type:<12} | GHC {tx_amount_ghc:<10,.2f} | GHC {bal_after_ghc:<10,.2f}")

    print("-" * global_width)
    print("\nPress ENTER to return to Account Operations...", end="")
    input()

# ==============================================================================
# UN-AUTHENTICATED MAIN SYSTEM WORKFLOW
# ==============================================================================
def main_menu(session):
    """Controls the primary unauthenticated main menu loop"""

    while True:
        main_banner()

        main_menu_options = [
            "Login to Existing Customer Account",
            "Register New Customer Profile",
            "Exit Application"
        ]

        # Enumerate and display main menu options
        for main_menu_index, main_menu_option in enumerate(main_menu_options, start=1):
            print(f"[{main_menu_index}]. {main_menu_option}")
        print()

        try:
            menu_choice = int(input("Select a menu choice (1-3): "))

            if menu_choice not in range(1, 4):
                print("Invalid menu choice! Option must be between 1 and 3.")
                sleep()
            elif menu_choice == 1:
                login_customer_workflow(session)
            elif menu_choice == 2:
                register_customer_workflow()
            elif menu_choice == 3:
                print("\nThank you for choosing CODE LEGION BANK!")
                loading_screen("Shutting down system")
                sys.exit()

        except ValueError:
            print("Input must be a valid number (1 - 3).")
            sleep()

if __name__ == "__main__":
    # Initializing the database before loading program UI
    db.initialize_database()
    # Starting full program test run
    bank_session = sess.UserSession()
    main_menu(bank_session)