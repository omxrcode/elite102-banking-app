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
    cursor.execute("SELECT name, balance FROM accounts WHERE name = %s", (name,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def create_account():
    name = input("Account holder name: ")
    if not name.strip():
        print("Name cannot be empty!")
        return
    try:
        balance = float(input("Initial deposit: $"))
    except ValueError:
        print("Invalid amount!")
        return
    if balance < 0:
        print("Initial deposit cannot be negative!")
        return
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", (name, balance))
        if balance > 0:
            cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'deposit', %s)", (name, balance))
        conn.commit()
        print(f"Account created for {name} with ${balance:.2f}")
    except:
        print("An account with that name already exists!")
    cursor.close()
    conn.close()

def deposit():
    name = input("Account name: ")
    row = find_account(name)
    if not row:
        print("Account not found!")
        return
    try:
        amount = float(input("Deposit amount: $"))
    except ValueError:
        print("Invalid amount!")
        return
    if amount <= 0:
        print("Amount must be positive.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    new_balance = float(row[1]) + amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE name = %s", (new_balance, name))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'deposit', %s)", (name, amount))
    conn.commit()
    print(f"Deposited ${amount:.2f}. New balance: ${new_balance:.2f}")
    cursor.close()
    conn.close()

def withdraw():
    name = input("Account name: ")
    row = find_account(name)
    if not row:
        print("Account not found!")
        return
    try:
        amount = float(input("Withdrawal amount: $"))
    except ValueError:
        print("Invalid amount!")
        return
    if amount <= 0:
        print("Amount must be positive.")
        return
    current = float(row[1])
    if amount > current:
        print(f"Not enough funds. Current balance: ${current:.2f}")
        return
    conn = get_connection()
    cursor = conn.cursor()
    new_balance = current - amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE name = %s", (new_balance, name))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'withdrawal', %s)", (name, amount))
    conn.commit()
    print(f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")
    cursor.close()
    conn.close()

def transfer():
    sender = input("From account: ")
    row_from = find_account(sender)
    if not row_from:
        print("Sender account not found!")
        return
    receiver = input("To account: ")
    row_to = find_account(receiver)
    if not row_to:
        print("Receiver account not found!")
        return
    if sender.lower() == receiver.lower():
        print("Cannot transfer to the same account!")
        return
    try:
        amount = float(input("Transfer amount: $"))
    except ValueError:
        print("Invalid amount!")
        return
    if amount <= 0:
        print("Amount must be positive.")
        return
    sender_balance = float(row_from[1])
    if amount > sender_balance:
        print(f"Not enough funds. {sender}'s balance: ${sender_balance:.2f}")
        return
    conn = get_connection()
    cursor = conn.cursor()
    new_sender = sender_balance - amount
    new_receiver = float(row_to[1]) + amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE name = %s", (new_sender, sender))
    cursor.execute("UPDATE accounts SET balance = %s WHERE name = %s", (new_receiver, receiver))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'transfer out', %s)", (sender, amount))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'transfer in', %s)", (receiver, amount))
    conn.commit()
    print(f"Transferred ${amount:.2f} from {sender} to {receiver}")
    print(f"  {sender}: ${new_sender:.2f}")
    print(f"  {receiver}: ${new_receiver:.2f}")
    cursor.close()
    conn.close()

def delete_account():
    name = input("Account name to delete: ")
    row = find_account(name)
    if not row:
        print("Account not found!")
        return
    balance = float(row[1])
    if balance > 0:
        print(f"Account still has ${balance:.2f}. Withdraw funds first!")
        return
    confirm = input(f"Are you sure you want to delete {name}'s account? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancelled.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE account_name = %s", (name,))
    cursor.execute("DELETE FROM accounts WHERE name = %s", (name,))
    conn.commit()
    print(f"Account for {name} has been deleted.")
    cursor.close()
    conn.close()

def check_balance():
    name = input("Account name: ")
    row = find_account(name)
    if not row:
        print("Account not found!")
    else:
        print(f"{row[0]}'s balance: ${float(row[1]):.2f}")

def show_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance FROM accounts ORDER BY name")
    rows = cursor.fetchall()
    if not rows:
        print("No accounts found.")
    else:
        total = 0
        print(f"\n{'Name':<20} {'Balance':>10}")
        print("-" * 32)
        for row in rows:
            bal = float(row[1])
            total += bal
            print(f"{row[0]:<20} ${bal:>9.2f}")
        print("-" * 32)
        print(f"{'Total':<20} ${total:>9.2f}")
        print(f"  {len(rows)} account(s)")
    cursor.close()
    conn.close()

def transaction_history():
    name = input("Account name: ")
    row = find_account(name)
    if not row:
        print("Account not found!")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, amount, created_at FROM transactions WHERE account_name = %s ORDER BY created_at DESC LIMIT 10", (name,))
    rows = cursor.fetchall()
    if not rows:
        print("No transactions found for this account.")
    else:
        print(f"\n--- Last transactions for {name} ---")
        print(f"{'Type':<15} {'Amount':>10}  {'Date'}")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]:<15} ${float(row[1]):>9.2f}  {row[2]}")
        print("-" * 50)
    cursor.close()
    conn.close()

def main_menu():
    print("\nConnecting to database...")
    try:
        conn = get_connection()
        conn.close()
        print("Connected!")
    except Exception as e:
        print(f"Could not connect to MySQL: {e}")
        print("Make sure MySQL Server is running.")
        return

    while True:
        print("\n===== Banking System =====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer Money")
        print("5. Check Balance")
        print("6. All Accounts")
        print("7. Transaction History")
        print("8. Delete Account")
        print("9. Exit")

        choice = input("\nChoose an option: ")

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
            delete_account()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()
