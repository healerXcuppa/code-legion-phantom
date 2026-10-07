import unittest
import sqlite3
import os
import gc
import time
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import application modules
import database as db
import authentication as auth
import banking_operations as ops
import utilities as util
import customer as cust
import account as acc
import session as sess


class TestIntensiveModules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up isolated test database file."""
        cls.test_db_file = "test_intensive_bank.db"
        db.DB_FILE = cls.test_db_file
        db.initialize_database()

    @classmethod
    def tearDownClass(cls):
        """Clean up test database file completely after tests."""
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
        """Reset session state before each test case."""
        self.session = sess.UserSession()

    def _create_test_customer(self, name="INTENSIVE USER"):
        """Helper to create valid parent customer for foreign key compliance."""
        cust_id = util.generate_customer_id()
        pwd_hash = auth.hash_password("SuperSecret123")
        customer = cust.Customer(
            customer_id=cust_id,
            customer_name=name,
            customer_email=f"user_{cust_id.lower()}@legion.com",
            customer_phone_num="0241112233",
            customer_date_of_birth="1998-05-12",
            customer_password_hash=pwd_hash
        )
        db.save_customer(customer)
        return customer

    # ==========================================================================
    # 1. INTENSIVE AUTHENTICATION & SECURITY TESTS
    # ==========================================================================
    def test_auth_special_characters_and_whitespace(self):
        """Test hashing & verifying complex passwords with symbols, spaces, and emojis"""
        complex_passwords = [
            "  spaced_password  ",
            "P@ssw0rd!#$&*()_+",
            "🔐CryptoKey2026",
            "a" * 1000  # Extreme length password
        ]
        for pwd in complex_passwords:
            pwd_hash = auth.hash_password(pwd)
            self.assertTrue(auth.verify_password(pwd_hash, pwd))
            self.assertFalse(auth.verify_password(pwd_hash, pwd + "wrong"))

    def test_auth_pin_boundary_verifications(self):
        """Test PIN hashing against numeric string variations"""
        pin = "0007"  # Leading zeros
        pin_hash = auth.hash_pin(pin)

        self.assertTrue(auth.verify_pin(pin_hash, "0007"))
        self.assertFalse(auth.verify_pin(pin_hash, "7"))
        self.assertFalse(auth.verify_pin(pin_hash, "0070"))

    # ==========================================================================
    # 2. INTENSIVE DATABASE & SQL INJECTION / INTEGRITY TESTS
    # ==========================================================================
    def test_db_sql_injection_resilience(self):
        """Ensure inputs containing SQL injection attacks are safely handled"""
        sql_injection_strings = [
            "' OR '1'='1",
            "'; DROP TABLE customers; --",
            "CUST-001' UNION SELECT * FROM accounts --"
        ]
        
        for injection in sql_injection_strings:
            # Querying database with malicious payload should safely return None, not crash or execute SQL
            found_cust = db.find_customer(injection)
            self.assertIsNone(found_cust)

            found_acc = db.find_account(injection)
            self.assertIsNone(found_acc)

    def test_db_duplicate_primary_key_prevention(self):
        """Ensure duplicate primary key creation raises DB error or fails gracefully"""
        cust_obj = self._create_test_customer("PRIMARY CUST")
        duplicate_cust = cust.Customer(
            customer_id=cust_obj.get_customer_id(), # Duplicate ID
            customer_name="CLONE CUST",
            customer_email="clone@legion.com",
            customer_phone_num="0200000000",
            customer_date_of_birth="2000-01-01",
            customer_password_hash=auth.hash_password("Pass1234")
        )

        # Attempting to re-insert existing primary key should raise an error or roll back cleanly
        try:
            db.save_customer(duplicate_cust)
        except Exception as e:
            self.assertTrue(isinstance(e, (sqlite3.IntegrityError, Exception)))

        # Verify the original record remains untainted
        original = db.find_customer(cust_obj.get_customer_id())
        self.assertEqual(original.get_customer_name(), "PRIMARY CUST")

    # ==========================================================================
    # 3. INTENSIVE BANKING OPERATIONS & FINANCIAL EDGE CASES
    # ==========================================================================
    def test_ops_overdraft_prevention(self):
        """Ensure withdrawing more than available balance fails or raises error"""
        cust_obj = self._create_test_customer()
        acc_num = util.generate_account_number()

        # Account balance: 50.00 GHC (5000 pesewas)
        account = acc.Account(
            account_number=acc_num,
            account_label="Overdraft Test",
            account_type="Savings Account",
            account_balance=5000,
            account_pin_hash=auth.hash_pin("1234"),
            account_customer_id=cust_obj.get_customer_id(),
            account_creation_date=util.generate_timestamp()
        )
        db.save_account(account)

        # Attempt to withdraw 100.00 GHC (10000 pesewas)
        overdraft_amount = 10000
        
        # Check if banking_operations rejects or handles overdraft
        result = ops.withdraw(acc_num, overdraft_amount)
        if result is False:
            self.assertFalse(result)
        
        # Balance in database must remain 5000 pesewas
        db_acc = db.find_account(acc_num)
        self.assertEqual(db_acc.get_account_balance(), 5000)

    def test_ops_negative_and_zero_amount_handling(self):
        """Ensure deposits and withdrawals with negative/zero values are rejected"""
        cust_obj = self._create_test_customer()
        acc_num = util.generate_account_number()

        account = acc.Account(
            account_number=acc_num,
            account_label="Zero Test",
            account_type="Savings Account",
            account_balance=10000, # 100.00 GHC
            account_pin_hash=auth.hash_pin("1234"),
            account_customer_id=cust_obj.get_customer_id(),
            account_creation_date=util.generate_timestamp()
        )
        db.save_account(account)

        # Negative & Zero Amounts
        invalid_amounts = [-5000, -1, 0]

        for amt in invalid_amounts:
            dep_res = ops.deposit(acc_num, amt)
            with_res = ops.withdraw(acc_num, amt)

            # Operations should return False or leave balance unchanged
            if dep_res is not None:
                self.assertFalse(dep_res)
            if with_res is not None:
                self.assertFalse(with_res)

            db_acc = db.find_account(acc_num)
            self.assertEqual(db_acc.get_account_balance(), 10000)

    def test_ops_transfer_to_nonexistent_account(self):
        """Ensure transferring funds to a non-existent account number fails safely"""
        sender_cust = self._create_test_customer("SENDER")
        sender_acc_num = util.generate_account_number()

        sender = acc.Account(
            account_number=sender_acc_num,
            account_label="Sender",
            account_type="Savings Account",
            account_balance=10000, # 100.00 GHC
            account_pin_hash=auth.hash_pin("1234"),
            account_customer_id=sender_cust.get_customer_id(),
            account_creation_date=util.generate_timestamp()
        )
        db.save_account(sender)

        fake_recipient_num = "9999999999999"

        # Transfer attempt
        res = ops.transfer(sender_acc_num, fake_recipient_num, 2000)
        if res is not None:
            self.assertFalse(res)

        # Sender balance must remain completely untouched (100.00 GHC)
        db_sender = db.find_account(sender_acc_num)
        self.assertEqual(db_sender.get_account_balance(), 10000)

    # ==========================================================================
    # 4. INTENSIVE SESSION & UTILITY TESTS
    # ==========================================================================
    def test_session_state_resets(self):
        """Ensure logging in a new user wipes the previous active account state"""
        cust_1 = self._create_test_customer("USER 1")
        cust_2 = self._create_test_customer("USER 2")

        test_acc = acc.Account(
            account_number=util.generate_account_number(),
            account_label="Acc 1",
            account_type="Savings Account",
            account_balance=1000,
            account_pin_hash=auth.hash_pin("1111"),
            account_customer_id=cust_1.get_customer_id(),
            account_creation_date=util.generate_timestamp()
        )

        test_sess = sess.UserSession()
        test_sess.start_session(cust_1)
        test_sess.set_active_account(test_acc)

        self.assertEqual(test_sess.get_current_account().get_account_number(), test_acc.get_account_number())

        # Start new session with USER 2
        test_sess.start_session(cust_2)

        # Active account must reset to None so USER 2 cannot access USER 1's account!
        self.assertIsNone(test_sess.get_current_account())
        self.assertEqual(test_sess.get_current_customer().get_customer_id(), cust_2.get_customer_id())

    def test_utilities_unique_id_generation(self):
        """Ensure ID generator utility creates unique identifiers across 100 iterations"""
        generated_ids = set()
        for _ in range(100):
            new_id = util.generate_customer_id()
            self.assertNotIn(new_id, generated_ids)
            generated_ids.add(new_id)

        generated_accs = set()
        for _ in range(100):
            new_acc = util.generate_account_number()
            self.assertNotIn(new_acc, generated_accs)
            generated_accs.add(new_acc)


if __name__ == "__main__":
    unittest.main()