"""
Handles banking operations for the CODE LEGION BANK.
Coordinates business logic between domain entities (Account, Transaction)
and the persistence layer (database.py).
"""

import database as db
import transaction as tx
import utilities as util

def deposit(account_number, amount):
    """Handles full atomic deposit operation."""
    # First check to ensure deposit amount is valid.
    if amount <= 0:
        print("Error: Deposit amount must be greater than zero.")
        return False

    try:
        # 1. Opening the database context manager
        with db.DatabaseConnection(db.db_path) as conn:

            # 2. Fetch the account domain object through the shared connection
            account_obj = db.find_account(account_number, conn=conn)
            if account_obj is None:
                print(f"Error: Account '{account_number}' not found.")
                return False

            # 3. Assigning existing account balance as balance before transaction.
            balance_before = account_obj.get_account_balance()

            # The account object handles it's deposit and assigns updated balance to balance after
            account_obj.deposit(amount)
            balance_after = account_obj.get_account_balance()

            # 4. Updating user balance to database
            balance_updated = db.update_account_balance(
                account_number=account_number,
                new_balance=balance_after,
                conn=conn
            )
            if not balance_updated:
                raise db.sqlite3.Error("Failed to update account balance in database.")

            # 5. Create the Transaction audit log record after a successful deposit.
            transaction_record = tx.Transaction(
                transaction_id=util.generate_transaction_id(),
                account_number=account_number,
                transaction_type="DEPOSIT",
                transaction_amount=amount,
                balance_before_transaction=balance_before,
                balance_after_transaction=balance_after,
                transaction_timestamp=util.generate_timestamp()
            )

            # 6. Ask database.py to persist the transaction record using the shared connection
            tx_saved = db.save_transaction(transaction_record, conn=conn)
            if not tx_saved:
                raise db.sqlite3.Error("Failed to persist transaction audit log.")

            # 7. Commit both changes together atomically!
            conn.commit()
            print(f"Success: Deposited {amount} pesewas into '{account_number}'.")
            return True

    except db.sqlite3.Error as error_message:
        print(f"Operation Error on Deposit: {error_message}")
        return False

def withdraw(account_number,amount):
    """Orchestrates the complete atomic withdrawal operation."""
    # First check to ensure withdrawal amount is valid.
    if amount <= 0:
        print("Error: withdrawal amount must be greater than zero.")
        return False

    try:
        # 1. Opening the database context manager
        with db.DatabaseConnection(db.db_path) as conn:

            # 2. Fetch the account domain object through the shared connection
            account_obj = db.find_account(account_number, conn=conn)
            if account_obj is None:
                print(f"Error: Account '{account_number}' not found.")
                return False

            # 3. Assigning existing account balance as balance before transaction.
            balance_before = account_obj.get_account_balance()

            # Guarding against insufficiant account balance.
            if amount > balance_before:
                print(f"Error: Insufficient funds. Available: {balance_before} pesewas.")
                return False

            # The account object handles the withdrawal and assigns updated balance to balance after
            account_obj.withdraw(amount)
            balance_after = account_obj.get_account_balance()

            # 4. Updating user balance to database
            balance_updated = db.update_account_balance(
                account_number=account_number,
                new_balance=balance_after,
                conn=conn
            )
            if not balance_updated:
                raise db.sqlite3.Error("Failed to update account balance in database.")

            # 5. Create the Transaction audit log record after a successful withdrawal.
            transaction_record = tx.Transaction(
                transaction_id=util.generate_transaction_id(),
                account_number=account_number,
                transaction_type="WITHDRAWAL",
                transaction_amount=amount,
                balance_before_transaction=balance_before,
                balance_after_transaction=balance_after,
                transaction_timestamp=util.generate_timestamp()
            )

            # 6. Ask database.py to persist the transaction record using the shared connection
            tx_saved = db.save_transaction(transaction_record, conn=conn)
            if not tx_saved:
                raise db.sqlite3.Error("Failed to persist transaction audit log.")

            # 7. Commit both changes together atomically!
            conn.commit()
            print(f"Success: Withdrawal of {amount} pesewas from '{account_number}'.")
            return True

    except db.sqlite3.Error as error_message:
        print(f"Operation Error on Withdrawal: {error_message}")
        return False

def transfer(sender_acc_num,receiver_acc_num,amount):
    """Transfers funds atomically between two accounts with double-entry transaction logging."""
    if sender_acc_num == receiver_acc_num:
        print("Error: Cannot transfer funds to the same account.")
        return False

    if amount <= 0:
        print("Error: Transfer amount must be greater than zero.")
        return False

    try:
        # 1. Opening the database context manager
        with db.DatabaseConnection(db.db_path) as conn:

            # 2. Fetch both account objects through shared connection
            sender_acc_obj = db.find_account(sender_acc_num,conn=conn)
            if sender_acc_obj is None:
                print(f"Error: Account '{sender_acc_num}' not found.")
                return False

            receiver_acc_obj = db.find_account(receiver_acc_num,conn=conn)
            if receiver_acc_obj is None:
                print(f"Error: Account '{receiver_acc_num}' not found.")
                return False

            # 3. Assigning existing account balance as balance before transaction.
            sender_balance_before = sender_acc_obj.get_account_balance()
            receiver_balance_before = receiver_acc_obj.get_account_balance()

            # Guarding against insufficiant account balance.
            if amount > sender_balance_before:
                print(f"Error: Insufficient funds. Available: {sender_balance_before} pesewas.")
                return False

            # Sender account handles withdrawal and Receiver handles the deposit.
            sender_acc_obj.withdraw(amount)
            sender_balance_after = sender_acc_obj.get_account_balance()

            receiver_acc_obj.deposit(amount)
            receiver_balance_after = receiver_acc_obj.get_account_balance()

            # 4. Updating sender and receiver account balance to database
            sender_balance_updated = db.update_account_balance(
                account_number=sender_acc_num,
                new_balance=sender_balance_after,
                conn=conn
            )
            if not sender_balance_updated:
                raise db.sqlite3.Error("Failed to update account balance in database.")

            receiver_balance_updated = db.update_account_balance(
                account_number=receiver_acc_num,
                new_balance=receiver_balance_after,
                conn=conn
            )
            if not receiver_balance_updated:
                raise db.sqlite3.Error("Failed to update account balance in database.")

            # 5. Create the Transaction audit log record after a successful transfer
            tx_timestamp = util.generate_timestamp()

            sender_tx = tx.Transaction(
                util.generate_transaction_id(),
                sender_acc_num,
                "TRANSFER_OUT",
                amount,
                sender_balance_before,
                sender_balance_after,
                tx_timestamp
            )

            receiver_tx = tx.Transaction(
                util.generate_transaction_id(),
                receiver_acc_num,
                "TRANSFER_IN",
                amount,
                receiver_balance_before,
                receiver_balance_after,
                tx_timestamp
            )

            # 6. Ask database.py to persist the transaction record using the shared connection
            if not db.save_transaction(sender_tx, conn=conn) \
                or not db.save_transaction(receiver_tx, conn=conn):
                raise db.sqlite3.Error("Failed to persist transfer transaction records.")

            # 7. Commit all operations together
            conn.commit()
            return True

    except db.sqlite3.Error as error_message:
        print(f"Database Error on Transfer: {error_message}")
        return False