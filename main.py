import sqlite3

    
def create_account(connection, name, age, balance):
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO banking (name, age, balance) VALUES (?, ?, ?)
    ''', (name, age, balance))
    print(f"Account created for {name} with balance {balance}")
    

def deposit(connection, account_id, amount): 
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM banking WHERE id = ?", (account_id,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found.")
        return

    update_balance = result[0] + amount

    cursor.execute("UPDATE banking SET balance = ? WHERE id = ?", (update_balance, account_id))
    connection.commit()

    print(f"Deposited {amount}. New balance: {update_balance}")


def withdraw(connection, account_id, amount):
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM banking WHERE id = ?", (account_id,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found.")
        return

    balance = result[0]

    if amount > balance:
        print("Insufficient funds.")
        return

    update_balance = balance - amount

    cursor.execute("UPDATE banking SET balance = ? WHERE id = ?", (update_balance, account_id))
    connection.commit()

    print(f"Withdrew {amount}. New balance: {update_balance}")

def check_balance(connection, account_id):
    cursor = connection.cursor()

    cursor.execute("SELECT name, balance FROM banking WHERE id = ?", (account_id,))
    result = cursor.fetchone()

    if result:
        print(f"{result[0]}'s balance: {result[1]}")
    else:
        print("Account cannot be found.")

def list_accounts(connection):
    cursor = connection.cursor()

    results = cursor.execute("SELECT * FROM banking")

    print("\nAll Accounts:")
    for row in results:
        print(row)

def main():
    connection = sqlite3.connect('example.db')

    while True:
        print("\nSunshine Bank")
        print("1 - Create Account")
        print("2 - Deposit")
        print("3 - Withdraw")
        print("4 - Check Balance")
        print("5 - Show Accounts")
        print("6 - Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Name: ")
            age = int(input("Age: "))
            balance = float(input("Initial deposit: "))
            create_account(connection, name, age, balance)
            connection.commit()

        elif choice == "2":
            account_id = int(input("Account ID: "))
            amount = float(input("Amount to deposit: "))
            deposit(connection, account_id, amount)

        elif choice == "3":
            account_id = int(input("Account ID: "))
            amount = float(input("Amount to withdraw: "))
            withdraw(connection, account_id, amount)

        elif choice == "4":
            account_id = int(input("Account ID: "))
            check_balance(connection, account_id)

        elif choice == "5":
            list_accounts(connection)

        elif choice == "6":
            break

        else:
            print("Invalid option.")

    connection.close()


if __name__ == "__main__":
    main()
