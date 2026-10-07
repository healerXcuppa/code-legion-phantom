"""Transaction Module to handle all transaction operations"""

class Transaction:
    """Blueprint for each transaction created in the bank system"""
    def __init__(
        self,
        transaction_id,
        account_number,
        transaction_type,
        transaction_amount,
        balance_before_transaction,
        balance_after_transaction,
        transaction_timestamp,
    ):
        self.__transaction_id = transaction_id
        self.__account_number = account_number
        self.__transaction_type = transaction_type
        self.__transaction_amount = transaction_amount
        self.__balance_before_transaction = balance_before_transaction
        self.__balance_after_transaction = balance_after_transaction
        self.__transaction_timestamp = transaction_timestamp

    # --- RETURN PRIVATE INSTANCE VARIABLES GETTERS ---
    def get_transaction_id(self):
        """Returns private transaction id"""
        return self.__transaction_id

    def get_account_number(self):
        """Returns private account number"""
        return self.__account_number

    def get_transaction_type(self):
        """Returns private transaction type"""
        return self.__transaction_type

    def get_transaction_amount(self):
        """Returns private transaction amount"""
        return self.__transaction_amount

    def get_balance_before(self):
        """Return private balance before transaction"""
        return self.__balance_before_transaction

    def get_balance_after(self):
        """Return private balance after transaction"""
        return self.__balance_after_transaction

    def get_transaction_timestamp(self):
        """Return private transaction timestamp"""
        return self.__transaction_timestamp