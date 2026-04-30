import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="banking_system"
    )

def create_account():
    name = input("Account holder name: ")
    balance = float(input("Initial deposit: $"))
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
    amount = float(input("Deposit amount: $"))
    if amount <= 0:
        print("Amount must be positive.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE name = %s", (name,))
    row = cursor.fetchone()
    if not row:
        print("Account not found!")
        cursor.close()
        conn.close()
        return
    new_balance = row[0] + amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE name = %s", (new_balance, name))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'deposit', %s)", (name, amount))
    conn.commit()
    print(f"Deposited ${amount:.2f}. New balance: ${new_balance:.2f}")
    cursor.close()
    conn.close()

def withdraw():
    name = input("Account name: ")
    amount = float(input("Withdrawal amount: $"))
    if amount <= 0:
        print("Amount must be positive.")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE name = %s", (name,))
    row = cursor.fetchone()
    if not row:
        print("Account not found!")
        cursor.close()
        conn.close()
        return
    if amount > row[0]:
        print(f"Not enough funds. Current balance: ${row[0]:.2f}")
        cursor.close()
        conn.close()
        return
    new_balance = row[0] - amount
    cursor.execute("UPDATE accounts SET balance = %s WHERE name = %s", (new_balance, name))
    cursor.execute("INSERT INTO transactions (account_name, type, amount) VALUES (%s, 'withdrawal', %s)", (name, amount))
    conn.commit()
    print(f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}")
    cursor.close()
    conn.close()

def check_balance():
    name = input("Account name: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE name = %s", (name,))
    row = cursor.fetchone()
    if not row:
        print("Account not found!")
    else:
        print(f"{name}'s balance: ${row[0]:.2f}")
    cursor.close()
    conn.close()

def show_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, balance FROM accounts")
    rows = cursor.fetchall()
    if not rows:
        print("No accounts found.")
    else:
        print(f"\n{'Name':<20} {'Balance':>10}")
        print("-" * 32)
        for row in rows:
            print(f"{row[0]:<20} ${row[1]:>9.2f}")
        print("-" * 32)
    cursor.close()
    conn.close()

def transaction_history():
    name = input("Account name: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT type, amount, created_at FROM transactions WHERE account_name = %s ORDER BY created_at DESC LIMIT 10", (name,))
    rows = cursor.fetchall()
    if not rows:
        print("No transactions found for this account.")
    else:
        print(f"\n--- Last transactions for {name} ---")
        print(f"{'Type':<12} {'Amount':>10}  {'Date'}")
        print("-" * 45)
        for row in rows:
            print(f"{row[0]:<12} ${row[1]:>9.2f}  {row[2]}")
        print("-" * 45)
    cursor.close()
    conn.close()

def main_menu():
    while True:
        print("\n===== Banking System =====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. All Accounts")
        print("6. Transaction History")
        print("7. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            show_accounts()
        elif choice == "6":
            transaction_history()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main_menu()
