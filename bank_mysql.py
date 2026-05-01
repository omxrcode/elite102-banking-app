import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="banking_system"
    )

def find_account(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance FROM accounts WHERE LOWER(name) = LOWER(%s)", (name,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def create_account():
    name = input("Enter account name: ")
    if find_account(name):
        print("Account already exists!")
        return
    balance = float(input("Enter starting balance: "))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
    if balance > 0:
        cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'deposit', %s)", (name, balance))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Account created for {name} with ${balance:.2f}")

def deposit():
    name = input("Enter account name: ")
    account = find_account(name)
    if not account:
        print("Account not found!")
        return
    amount = float(input("How much to deposit? "))
    new_balance = float(account[1]) + amount
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = %s WHERE LOWER(name) = LOWER(%s)", (new_balance, name))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'deposit', %s)", (account[0], amount))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Deposited ${amount:.2f}. New balance: ${new_balance:.2f}")

def withdraw():
    name = input("Enter account name: ")
    account = find_account(name)
    if not account:
        print("Account not found!")
        return
    amount = float(input("How much to withdraw? "))
    current = float(account[1])
    if amount > current:
        print("Not enough money!")
        return
    new_balance = current - amount
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = %s WHERE LOWER(name) = LOWER(%s)", (new_balance, name))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'withdrawal', %s)", (account[0], amount))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")

def transfer():
    sender = input("Transfer from: ")
    account_from = find_account(sender)
    if not account_from:
        print("Account not found!")
        return
    receiver = input("Transfer to: ")
    account_to = find_account(receiver)
    if not account_to:
        print("Account not found!")
        return
    amount = float(input("How much to transfer? "))
    sender_balance = float(account_from[1])
    if amount > sender_balance:
        print("Not enough money!")
        return
    new_sender = sender_balance - amount
    new_receiver = float(account_to[1]) + amount
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance = %s WHERE LOWER(name) = LOWER(%s)", (new_sender, sender))
    cursor.execute("UPDATE accounts SET balance = %s WHERE LOWER(name) = LOWER(%s)", (new_receiver, receiver))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'transfer out', %s)", (account_from[0], amount))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'transfer in', %s)", (account_to[0], amount))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Transferred ${amount:.2f} from {account_from[0]} to {account_to[0]}")

def check_balance():
    name = input("Enter account name: ")
    account = find_account(name)
    if not account:
        print("Account not found!")
        return
    print(f"{account[0]}'s balance: ${float(account[1]):.2f}")

def show_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance FROM accounts ORDER BY name")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if not rows:
        print("No accounts yet.")
        return
    print("\n--- All Accounts ---")
    for row in rows:
        print(f"{row[0]}: ${float(row[1]):.2f}")
    print("--------------------")

def transaction_history():
    name = input("Enter account name: ")
    account = find_account(name)
    if not account:
        print("Account not found!")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, amount, created_at FROM transactions WHERE account_name = %s ORDER BY created_at DESC LIMIT 10", (account[0],))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if not rows:
        print("No transactions yet.")
        return
    print(f"\n--- Transactions for {account[0]} ---")
    for row in rows:
        print(f"  {row[0]}: ${float(row[1]):.2f}  ({row[2]})")
    print("--------------------")

def main_menu():
    while True:
        print("\n1. Create account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer money")
        print("5. Check balance")
        print("6. Show all accounts")
        print("7. Transaction history")
        print("8. Exit")

        choice = input("Pick an option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            transfer()
        elif choice == "5":
            check_balance()
        elif choice == "6":
            show_accounts()
        elif choice == "7":
            transaction_history()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main_menu()
