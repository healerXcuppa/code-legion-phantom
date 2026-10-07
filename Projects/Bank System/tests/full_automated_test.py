import unittest
import os
import gc
import time
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database as db
import authentication as auth
import banking_operations as ops
import utilities as util
import customer as cust
import account as acc
import session as sess

class TestMasterProgramLifecycle(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up an isolated test database for full lifecycle testing."""
        cls.test_db_file = "test_master_bank.db"
        db.DB_FILE = cls.test_db_file
        db.initialize_database()

    @classmethod
    def tearDownClass(cls):
        """Clean up and delete test database file upon test completion."""
        gc.collect()
        time.sleep(0.5)
        for extra_ext in ["", "-wal", "-shm", "-journal"]:
            file_path = f"{cls.test_db_file}{extra_ext}"
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    time.sleep(0.5)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        print(f"\n[WARNING] Could not auto-delete {file_path}: {e}")

    def setUp(self):
        """Reset session state before each test scenario."""
        self.session = sess.UserSession()

    # ==========================================================================
    # FULL END-TO-END SYSTEM LIFECYCLE SIMULATION
    # ==========================================================================
    def test_full_bank_system_lifecycle(self):
        """Simulate an end-to-end customer journey from registration to transfer auditing"""
        
        # ----------------------------------------------------------------------
        # STAGE 1: LEVEL 0 - CUSTOMER REGISTRATION
        # ----------------------------------------------------------------------
        sender_cust_id = util.generate_customer_id()
        sender_password = "MasterPassword123"
        sender_hash = auth.hash_password(sender_password)

        sender_customer = cust.Customer(
            customer_id=sender_cust_id,
            customer_name="SENDER LEGION",
            customer_email="sender@legion.com",
            customer_phone_num="0241112222",
            customer_date_of_birth="1995-10-15",
            customer_password_hash=sender_hash
        )
        db.save_customer(sender_customer)

        recipient_cust_id = util.generate_customer_id()
        recipient_customer = cust.Customer(
            customer_id=recipient_cust_id,
            customer_name="RECIPIENT LEGION",
            customer_email="recipient@legion.com",
            customer_phone_num="0203334444",
            customer_date_of_birth="1998-12-01",
            customer_password_hash=auth.hash_password("Pass5678")
        )
        db.save_customer(recipient_customer)

        # ----------------------------------------------------------------------
        # STAGE 2: LEVEL 1 - AUTHENTICATION & SESSION INITIATION
        # ----------------------------------------------------------------------
        # Verify invalid login fails
        fetched_sender = db.find_customer(sender_cust_id)
        self.assertIsNotNone(fetched_sender)
        self.assertFalse(auth.verify_password(fetched_sender.get_customer_password_hash(), "WrongPassword"))
        
        # Verify valid login succeeds and binds to session
        self.assertTrue(auth.verify_password(fetched_sender.get_customer_password_hash(), sender_password))
        self.session.start_session(fetched_sender)
        self.assertTrue(self.session.is_authenticated())

        # ----------------------------------------------------------------------
        # STAGE 3: LEVEL 2 - ACCOUNTS CREATION & PROFILE MANAGEMENT
        # ----------------------------------------------------------------------
        # 1. Update Sender Email
        new_sender_email = "sender_updated@legion.com"
        db.update_customer_email(sender_cust_id, new_sender_email)
        fetched_sender.change_email(new_sender_email)
        self.assertEqual(fetched_sender.get_customer_email(), new_sender_email)

        # 2. Create Accounts for Sender
        sender_acc_num1 = util.generate_account_number()
        sender_pin_hash1 = auth.hash_pin("1234")
        acc1 = acc.Account(
            account_number=sender_acc_num1,
            account_label="Primary Vault",
            account_type="Savings Account",
            account_balance=0,
            account_pin_hash=sender_pin_hash1,
            account_customer_id=sender_cust_id,
            account_creation_date=util.generate_timestamp()
        )
        db.save_account(acc1)

        # 3. Create Account for Recipient
        recipient_acc_num = util.generate_account_number()
        recipient_acc = acc.Account(
            account_number=recipient_acc_num,
            account_label="Recipient Main",
            account_type="Current Account",
            account_balance=0,
            account_pin_hash=auth.hash_pin("9999"),
            account_customer_id=recipient_cust_id,
            account_creation_date=util.generate_timestamp()
        )
        db.save_account(recipient_acc)

        # 4. Bind Sender Account 1 to Session
        sender_accounts = db.get_customer_accounts(sender_cust_id)
        self.assertEqual(len(sender_accounts), 1)
        active_account = sender_accounts[0]
        self.session.set_active_account(active_account)

        # ----------------------------------------------------------------------
        # STAGE 4: LEVEL 3 - BANKING OPERATIONS (DEPOSIT, WITHDRAW, TRANSFER)
        # ----------------------------------------------------------------------
        active_acc_num = active_account.get_account_number()

        # Step 1: Deposit GH₵ 500.00 (50000 pesewas)
        ops.deposit(active_acc_num, 50000)
        active_account.deposit(50000)
        self.assertEqual(active_account.get_account_balance(), 50000)

        # Step 2: Withdraw GH₵ 100.00 (10000 pesewas)
        # Verify PIN check authorization
        self.assertTrue(auth.verify_pin(active_account.get_account_pin_hash(), "1234"))
        ops.withdraw(active_acc_num, 10000)
        active_account.withdraw(10000)
        self.assertEqual(active_account.get_account_balance(), 40000)

        # Step 3: Transfer GH₵ 150.00 (15000 pesewas) to Recipient
        ops.transfer(active_acc_num, recipient_acc_num, 15000)
        active_account.withdraw(15000)
        recipient_acc.deposit(15000)

        # Check final balances in memory & database
        # Sender expected balance: 50000 - 10000 - 15000 = 25000 pesewas (GH₵ 250.00)
        self.assertEqual(active_account.get_account_balance(), 25000)
        db_sender_acc = db.find_account(active_acc_num)
        self.assertEqual(db_sender_acc.get_account_balance(), 25000)

        # Recipient expected balance: 0 + 15000 = 15000 pesewas (GH₵ 150.00)
        db_recipient_acc = db.find_account(recipient_acc_num)
        self.assertEqual(db_recipient_acc.get_account_balance(), 15000)

        # ----------------------------------------------------------------------
        # STAGE 5: LEVEL 3 - AUDIT TRAIL & TRANSACTION HISTORY VERIFICATION
        # ----------------------------------------------------------------------
        sender_logs = db.get_transaction(active_acc_num)
        # Expecting 3 transactions: DEPOSIT, WITHDRAWAL, TRANSFER_OUT
        self.assertEqual(len(sender_logs), 3)

        recipient_logs = db.get_transaction(recipient_acc_num)
        # Expecting 1 transaction: TRANSFER_IN
        self.assertEqual(len(recipient_logs), 1)

        # ----------------------------------------------------------------------
        # STAGE 6: SESSION TERMINATION
        # ----------------------------------------------------------------------
        self.session.clear_session()
        self.assertFalse(self.session.is_authenticated())
        self.assertIsNone(self.session.get_current_customer())
        self.assertIsNone(self.session.get_current_account())


if __name__ == "__main__":
    unittest.main()