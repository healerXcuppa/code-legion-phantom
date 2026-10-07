"""Database Connection and Query for Bank System"""
import sqlite3
from pathlib import Path
import customer as cust
import account as acc
import transaction as tx

# Establishing context manager error handling for database connection
class DatabaseConnection:
    """Class that handles the database connection"""
    def __init__(self, db_name):
        self.db_name = db_name
        # self.conn is the variable instance for holding the database connection
        self.conn = None

    def __enter__(self):
        # 1. Establish database connection
        self.conn = sqlite3.connect(self.db_name)

        # Turning on foreign key support for SQLite
        self.conn.execute("PRAGMA foreign_keys = ON;")
        print("Database Connected successfully.")

        # Return the active connection that of the created(connected) database
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # 2. An error happened: ROLL BACK and log the issue

            error_line_num = exc_tb.tb_lineno
            print("\n--- DEBUG LOG ---")
            print(f"Error Type: {exc_type.__name__}")
            print(f"Error Line Number: {error_line_num}")
            print(f"Database Error detected: {exc_val}")
            print("\nDatabase Rolling back all uncommitted changes...")

            # Rollback of database
            self.conn.rollback()

            # Close connection safely
            self.conn.close()
            print("Database Connection closed after failure.")

            # Return False to catch error
            return False
        else:
            # 3. No error happened: Close the connection
            self.conn.close()
            print("Database Connection closed successfully.")

            # Return False to catch error even though at this point there isn't any
            return False

# getting file path and getting database from the data folder
file_path = Path(__file__).resolve().parent
db_path = file_path / "data" / "bank.db"

def initialize_database():
    """Initializing database structure and tables"""

    db_tables = [
        """CREATE TABLE IF NOT EXISTS customers(
                customer_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                customer_email TEXT UNIQUE NOT NULL,
                customer_phone_num TEXT NOT NULL,
                customer_date_of_birth DATE NOT NULL,
                customer_password_hash TEXT NOT NULL
        );""",
        """CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                account_label TEXT NOT NULL,
                account_type TEXT NOT NULL,
                account_balance INTEGER NOT NULL
                    CHECK (account_balance >= 0),
                account_pin_hash TEXT NOT NULL,
                account_customer_id TEXT NOT NULL, 
                account_creation_date DATE NOT NULL,
                FOREIGN KEY (account_customer_id) 
                    REFERENCES customers (customer_id),
                UNIQUE (account_customer_id, account_label)
        );""",
        """CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                account_number TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                transaction_amount INTEGER NOT NULL
                    CHECK (transaction_amount > 0),
                balance_before INTEGER NOT NULL
                    CHECK (balance_before >= 0),
                balance_after INTEGER NOT NULL
                    CHECK (balance_after >= 0),
                transaction_date DATE NOT NULL,
                FOREIGN KEY (account_number) REFERENCES accounts (account_number)
        );"""
    ]

    # Establsihing the databse connection and catching errors if any
    try:
        with DatabaseConnection(db_path) as conn:
            # cursor for database query execution
            cursor = conn.cursor()

            # Executing table creation queries
            for create_table in db_tables:
                cursor.execute(create_table)

            # Committing changes to the database
            conn.commit()
    except sqlite3.Error as error_message:
        print(f"Database Error: {error_message}")

def save_customer(customer):
    """Saves a customer to the database"""

    # Creates a variable for parameterized data
    new_customer = """
        INSERT INTO customers (
        customer_id,
        customer_name,
        customer_email,
        customer_phone_num,
        customer_date_of_birth,
        customer_password_hash
    )
    VALUES(
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    );
    """

    # Establishing connection with the database and error handling
    try:
        with DatabaseConnection(db_path) as conn:
            # cursor for database query execution
            cursor = conn.cursor()

            # Executing query statements to database
            cursor.execute(
                new_customer,
                (
                    customer.get_customer_id(),
                    customer.get_customer_name(),
                    customer.get_customer_email(),
                    customer.get_customer_phone_num(),
                    customer.get_customer_date_of_birth(),
                    customer.get_customer_password_hash()
                )
            )

            # Commiting changes to database after query execution
            conn.commit()
            return True
    except sqlite3.Error as error_message:
        print(f"Database Error with Insert: {error_message}")
        return False

def find_customer(customer_id,conn=None):
    """Finds a customer by their customer id in the database"""

    # Query for customer search by customer id condition
    search_query = """
        SELECT
            customer_id,
            customer_name,
            customer_email,
            customer_phone_num,
            customer_date_of_birth,
            customer_password_hash
        FROM customers 
        WHERE customer_id = ?;
    """

    def _execute_find(active_conn):
        """Returns reconstructed customer obj when the customer is found and None if not"""
        cursor = active_conn.cursor()
        cursor.execute(search_query, (customer_id,))
        result = cursor.fetchone()
        if result:
            return cust.Customer(
                result[0],  # customer_id
                result[1],  # customer_name
                result[2],  # customer_email
                result[3],  # customer_phone_num
                result[4],  # customer_date_of_birth
                result[5]   # customer_password_hash
            )
        else:
            return None

    # Conditional block to handle conn connection before local function execution
    if conn is not None:
        try:
            return _execute_find(conn)
        except sqlite3.Error as error_message:
            print(f"Database Error on Customer Select (Shared Conn): {error_message}")
            return None

    # This happens automatically when the above condition is False
    try:
        with DatabaseConnection(db_path) as local_conn:
            return _execute_find(local_conn)
    except sqlite3.Error as error_message:
        print(f"Database Error on Customer Select: {error_message}")
        return None

def save_account(account):
    """Saves an account object to the database."""

    # Query for saving account into databse
    query = """
        INSERT INTO accounts (
            account_number,
            account_label,
            account_type,
            account_balance,
            account_pin_hash,
            account_customer_id,
            account_creation_date
        )
        VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );
    """

    # Establishing connection with the database and error handling
    try:
        with DatabaseConnection(db_path) as conn:

            #  cursor for database query execution
            cursor = conn.cursor()

            # Executing query statements to databasE
            cursor.execute(
                query,
                (
                    account.get_account_number(),
                    account.get_account_label(),
                    account.get_account_type(),
                    account.get_account_balance(),
                    account.get_account_pin_hash(),
                    account.get_account_customer_id(),
                    account.get_account_creation_date(),
                )
            )

            # Committing changes to database after query execution
            conn.commit()
            return True
    except sqlite3.Error as error_message:
        print(f"Database Error on Account Insert: {error_message}")
        return False

def find_account(account_number,conn=None):
    """Finds an account by number and reconstructs the Account object."""
    query = """
        SELECT
            account_number,
            account_label,
            account_type,
            account_balance,
            account_pin_hash,
            account_customer_id,
            account_creation_date
        FROM accounts
        WHERE account_number = ?;
    """

    # Local execution function to handle query execution regardless of active or new connection
    def _execute_find(active_conn):
        """Returns reconstructed account when account number found and None if not found."""
        cursor = active_conn.cursor()
        cursor.execute(query, (account_number,))
        result = cursor.fetchone()
        if result:
            return acc.Account(
                result[0],   #account_number
                result[1],    #account_label
                result[2], #account_type
                result[3],  #account_balance
                result[4], #account_pin_hash
                result[5],  #account_customer_id
                result[6]    #account_creation_date
            )
        return None

    # Conditional block to handle conn connection before local function execution
    if conn is not None:
        try:
            return _execute_find(conn)
        except sqlite3.Error as error_message:
            print(f"Database Error on Account Select (Shared Conn): {error_message}")
            return None

    # This happens automatically when the above condition is False
    try:
        with DatabaseConnection(db_path) as local_conn:
            return _execute_find(local_conn)
    except sqlite3.Error as error_message:
        print(f"Database Error on Account Select: {error_message}")
        return None

def save_transaction(transaction,conn=None):
    """Saves an immutable transaction audit log record to the database."""
    # Query statement with parameterized values
    query = """
        INSERT INTO transactions (
            transaction_id,
            account_number,
            transaction_type,
            transaction_amount,
            balance_before,
            balance_after,
            transaction_date
        ) 
        VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        );
    """

    # Query parametrized values
    query_values = (
        transaction.get_transaction_id(),
        transaction.get_account_number(),
        transaction.get_transaction_type(),
        transaction.get_transaction_amount(),
        transaction.get_balance_before(),
        transaction.get_balance_after(),
        transaction.get_transaction_timestamp()
    )

    # Checking if conn is suplied or not to continue implementation
    if conn is None:
        # Establishes new connection if conn parameter is None and tries query execution
        try:
            with DatabaseConnection(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    query,
                    query_values
                )

                # Commit and return True upon successful query execution
                conn.commit()
                return True

        except sqlite3.Error as error_message:
            print(f"Database Error on Transaction Insert: {error_message}")
            return False
    else:
        # Try and error handling query execution if conn parameter is not None
        try:
            cursor = conn.cursor()
            cursor.execute(
                query,
                query_values
            )

            # Returns True upon succesful query execution
            return True
        except sqlite3.Error as error_message:
            print(f"Database Error on Transaction Insert: {error_message}")
            return False

def get_transaction(account_number):
    """Retrieves all transaction logs for an account and reconstructs Transaction objects."""
    query = """
        SELECT
            transaction_id,
            account_number,
            transaction_type,
            transaction_amount,
            balance_before,
            balance_after,
            transaction_date
        FROM transactions
        WHERE account_number = ?
        ORDER BY transaction_date ASC;
    """
    try:
        with DatabaseConnection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (account_number,)
            )
            rows = cursor.fetchall()

            transaction_list = []
            for row in rows:
                transaction = tx.Transaction(
                    row[0],  # transaction_id
                    row[1],  # account_number
                    row[2],    # transaction_type
                    row[3],  # transaction_amount
                    row[4],  # balance_before_transaction
                    row[5],   # balance_after_transaction
                    row[6],   # transaction_timestamp
                )
                transaction_list.append(transaction)

            return transaction_list
    except sqlite3.Error as error_message:
        print(f"Database Error on Transaction Select: {error_message}")
        return []

def update_account_balance(account_number, new_balance, conn=None):
    """Updates the raw account balance in Database."""
    query = """
        UPDATE accounts
        SET account_balance = ?
        WHERE account_number = ?;
    """

    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, (new_balance, account_number))
            return True
        except sqlite3.Error as error_message:
            print(f"Database Error on Balance Update (Shared Conn): {error_message}")
            return False

    try:
        with DatabaseConnection(db_path) as local_conn:
            cursor = local_conn.cursor()
            cursor.execute(query, (new_balance, account_number))
            local_conn.commit()
            return True
    except sqlite3.Error as error_message:
        print(f"Database Error on Balance Update: {error_message}")
        return False

def update_customer_email(customer_id, new_email):
    """Updates the customer's email address in the database"""
    query = """
        UPDATE customers
        SET customer_email = ?
        WHERE customer_id = ?;
    """
    try:
        with DatabaseConnection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query,(new_email,customer_id))
            conn.commit()
    except sqlite3.Error as error_message:
        print(f"Database Error on Email Change: {error_message}")
        return False

def update_customer_phone(customer_id, new_phone):
    """Updates the customer's phone number in the database"""
    query = """
        UPDATE customers
        SET customer_phone_num = ?
        WHERE customer_id = ?;
    """
    try:
        with DatabaseConnection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query,(new_phone,customer_id))
            conn.commit()
    except sqlite3.Error as error_message:
        print(f"Database Error on Phone Number Change: {error_message}")
        return False

def get_customer_accounts(customer_id,conn=None):
    """Returns all accounts objects linked to a single customer"""
    query = """
        SELECT 
            account_number,
            account_label,
            account_type,
            account_balance,
            account_pin_hash,
            account_customer_id,
            account_creation_date
        FROM accounts
        WHERE account_customer_id =?;
    """

    def _execute_search(active_conn):
        """Returns a list of reconstructed found accounts and empty list if none is found"""
        cursor = active_conn.cursor()
        cursor.execute(
            query,
            (customer_id,)
        )
        results = cursor.fetchall()

        # Found Accounts reconnstruction and appending
        accounts = []
        for result in results:
            account = acc.Account(
                result[0],   #account_number
                result[1],    #account_label
                result[2], #account_type
                result[3],  #account_balance
                result[4], #account_pin_hash
                result[5],  #account_customer_id
                result[6]    #account_creation_date
            )
            # Apending reconstructed account
            accounts.append(account)
        if accounts:
            return accounts
        return []

    # Conditional block to handle conn connection before local function execution
    if conn is not None:
        try:
            return _execute_search(conn)
        except sqlite3.Error as error_message:
            print(f"Database Error on Account Search (Shared Conn): {error_message}")
            return None

    # This happens automatically when the above condition is False
    try:
        with DatabaseConnection(db_path) as local_conn:
            return _execute_search(local_conn)
    except sqlite3.Error as error_message:
        print(f"Database Error on Account Search: {error_message}")
        return None