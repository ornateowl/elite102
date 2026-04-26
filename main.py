import sqlite3

    
def create_account(connection, name, age, balance):
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO bank (name, age, balance) VALUES (?, ?, ?)
    ''', (name, age, balance))
    personal_id = cursor.lastrowid


    #add on to the transactions aspect
    if balance > 0:
        cursor.execute(
            "INSERT INTO transactions (personal_id, type, amount) VALUES (?, ?, ?)",
            (personal_id, "deposit", balance)
        )

    connection.commit()
    return personal_id

    print(f"Account created for {name} with balance {balance}")
    

def deposit(connection, personal_id, amount): 
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM bank WHERE id = ?", (personal_id,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found.")
        return

    update_balance = result[0] + amount

    cursor.execute("UPDATE bank SET balance = ? WHERE id = ?", (update_balance, personal_id))
    connection.commit()

    print(f"Deposited {amount}. New balance: {update_balance}")


def withdraw(connection, personal_id, amount):
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM bank WHERE id = ?", (personal_id,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found or does not exist.")
        return

    balance = result[0]

    if amount > balance:
        print("Insufficient funds.")
        return

    update_balance = balance - amount

    cursor.execute("UPDATE bank SET balance = ? WHERE id = ?", (update_balance, personal_id))
    connection.commit()

    print(f"Withdrew {amount}. New balance: {update_balance}")

def get_balance(connection, personal_id):
    cursor = connection.cursor()

    cursor.execute("SELECT name, balance FROM bank WHERE id = ?", (personal_id,))
    result = cursor.fetchone()

    if result:
        print(f"{result[0]}'s balance: {result[1]}")
    else:
        print("Account cannot be found.")

def list_accounts(connection):
    cursor = connection.cursor()

    results = cursor.execute("SELECT * FROM bank")

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
            personal_id = int(input("Account ID: "))
            amount = float(input("Amount to deposit: "))
            deposit(connection, personal_id, amount)

        elif choice == "3":
            personal_id = int(input("Account ID: "))
            amount = float(input("Amount to withdraw: "))
            withdraw(connection, personal_id, amount)

        elif choice == "4":
            personal_id = int(input("Account ID: "))
            get_balance(connection, personal_id)

        elif choice == "5":
            list_accounts(connection)

        elif choice == "6":
            break

        else:
            print("Please choose an option from the menu.")

    connection.close()


if __name__ == "__main__":
    main()
