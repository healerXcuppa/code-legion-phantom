"""Handles User session across program run"""

class UserSession:
    """Blueprint of the Session is going to be handle across the program"""
    def __init__(self):
        """Initial session state"""
        self.current_customer = None  # Holds Customer object when authenticated
        self.current_account = None   # Holds active Account object selected by user

    def is_authenticated(self):
        """Returns True if a customer is logged in."""
        return self.current_customer is not None

    def start_session(self, customer_obj):
        """Logs in a customer and binds their profile to the session."""
        self.current_customer = customer_obj
        self.current_account = None  # Reset active account on new login

    def set_active_account(self, account_obj):
        """Selects a specific account for financial operations."""
        self.current_account = account_obj

    def get_current_customer(self):
        """Returns the currently logged-in customer object."""
        return self.current_customer

    def get_current_account(self):
        """Returns the currently selected account object."""
        return self.current_account

    def clear_session(self):
        """Logs out the user and clears user session records."""
        self.current_customer = None
        self.current_account = None