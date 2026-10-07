"""Module for Customer creation and management."""

class Customer:
    """Represents a customer in the banking system."""
    # Instance variables for customer attributes
    def __init__(
        self,
        customer_id,
        customer_name,
        customer_email,
        customer_phone_num,
        customer_date_of_birth,
        customer_password_hash
    ):
        self.__customer_id = customer_id
        self.__customer_name = customer_name
        self._customer_email = customer_email
        self._customer_phone_num = customer_phone_num
        self.__customer_date_of_birth = customer_date_of_birth
        self.__customer_password_hash = customer_password_hash

    # --- RETURN PRIVATE AND PROTECTED ATTRIBUTES ---
    def get_customer_id(self):
        """Returns private customer id"""
        return self.__customer_id

    def get_customer_name(self):
        """Returns private customer name"""
        return self.__customer_name

    def get_customer_email(self):
        """Returns protected customer email"""
        return self._customer_email

    def get_customer_phone_num(self):
        """Returns protected phone number"""
        return self._customer_phone_num

    def get_customer_date_of_birth(self):
        """Returns private customer date of birth"""
        return self.__customer_date_of_birth

    def get_customer_password_hash(self):
        """Returns private customer passwword hash"""
        return self.__customer_password_hash

    # --- METHODS TO CHANGE CUSTOMER ATTRIBUTE ---
    def change_email(self,new_customer_email):
        """Operation to change a customer email"""
        self._customer_email = new_customer_email
        return self._customer_email

    def change_phone(self,new_customer_phone_num):
        """Operation to change and return new updated phone number"""
        self._customer_phone_num = new_customer_phone_num
        return self._customer_phone_num