"""Account Model to handle account related operations."""

class Account:
    """Blueprint for each account created in the bank system"""
    def __init__(
        self,
        account_number,
        account_label,
        account_type,
        account_balance,
        account_pin_hash,
        account_customer_id,
        account_creation_date
    ):
        self.__account_number = account_number
        self._account_label = account_label
        self._account_type = account_type
        self.__account_balance = account_balance
        self.__account_pin_hash = account_pin_hash
        self.__account_customer_id = account_customer_id
        self.__account_creation_date = account_creation_date

    # --- READ-ONLY GETTERS ---
    def get_account_number(self):
        """Returns private account number."""
        return self.__account_number

    def get_account_label(self):
        """Returns protected account label"""
        return self._account_label

    def get_account_type(self):
        """Returns protected account type"""
        return self._account_type

    def get_account_balance(self):
        """Returns private account balance."""
        return self.__account_balance

    def get_account_customer_id(self):
        """Returns customer ID of the account owner."""
        return self.__account_customer_id

    def get_account_pin_hash(self):
        """Returns stored PIN hash string."""
        return self.__account_pin_hash

    def get_account_creation_date(self):
        """Returns account creation date string."""
        return self.__account_creation_date

    # --- MUTATION OPERATIONS ---
    def change_label(self, new_account_label):
        """Updates account label."""
        self._account_label = new_account_label
        return self._account_label

    def change_account_pin(self,new_account_pin):
        """Returns updated account pin"""
        self.__account_pin_hash = new_account_pin
        return self.__account_pin_hash

    def deposit(self,deposit_amount):
        """Returns updated balance after a successful deposit"""
        if deposit_amount <= 0:
            return (False, self.__account_balance)

        self.__account_balance += deposit_amount
        return (True, self.__account_balance)

    def withdraw(self,withdraw_amount):
        """Returns updated balance after a successful withdrawal"""
        if withdraw_amount <= 0 or withdraw_amount > self.__account_balance:
            return (False, self.__account_balance)

        self.__account_balance -= withdraw_amount
        return (True, self.__account_balance)