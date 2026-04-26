import unittest

import sqlite3

from main import create_account, deposit, withdraw, get_balance

class bank_unit_test(unittest.TestCase):

    def test_func(self):
        # Fresh database for every test
        self.connection = sqlite3.connect(":memory:")
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE bank (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                balance REAL
            )
        ''')

        cursor.execute('''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                personal_id INTEGER,
                type TEXT,
                amount REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.connection.commit()

    def tearDown(self):
        self.connection.close()

    # ---- TESTS ----

    def test_create_account(self):
        account_id = create_account(self.connection, "Alice", 40, 100)

        balance = get_balance(self.connection, account_id)
        self.assertEqual(balance, 100)

    def test_deposit(self):
        account_id = create_account(self.connection, "Bob", 20, 50)

        result = deposit(self.connection, account_id, 30)
        self.assertTrue(result)

        balance = get_balance(self.connection, account_id)
        self.assertEqual(balance, 30)

    def test_withdraw(self):
        account_id = create_account(self.connection, "Silly", 24, 110)

        result = withdraw(self.connection, account_id, 60)
        self.assertTrue(result)

        balance = get_balance(self.connection, account_id)
        self.assertEqual(balance, 60)

    def test_withdraw_insufficient(self):
        account_id = create_account(self.connection, "Randy", 18, 10)

        result = withdraw(self.connection, account_id, 10)
        self.assertFalse(result)

    def test_negative_deposit(self):
        account_id = create_account(self.connection, "Lucky", 19, 77)

        result = deposit(self.connection, account_id, -10)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()