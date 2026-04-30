accounts = []

def find_account(name):
    for account in accounts:
        if account["name"].lower() == name.lower():
            return account
    return None

def create_account():
    name = input("Enter account name: ")
    if find_account(name):
        print("Account already exists!")
        return
    balance = float(input("Enter starting balance: "))
    accounts.append({"name": name, "balance": balance})
    print(f"Account created for {name} with ${balance:.2f}")

def deposit():
    name = input("Enter account name: ")
    account = find_account(name)
    if not account:
        print("Account not found!")
        return
    amount = float(input("How much to deposit? "))
    account["balance"] += amount
    print(f"Deposited ${amount:.2f}. New balance: ${account['balance']:.2f}")

def withdraw():
    name = input("Enter account name: ")
    account = find_account(name)
    if not account:
        print("Account not found!")
        return
    amount = float(input("How much to withdraw? "))
    if amount > account["balance"]:
        print("Not enough money!")
        return
    account["balance"] -= amount
    print(f"Withdrew ${amount:.2f}. New balance: ${account['balance']:.2f}")

def check_balance():
    name = input("Enter account name: ")
    account = find_account(name)
    if not account:
        print("Account not found!")
        return
    print(f"{account['name']}'s balance: ${account['balance']:.2f}")

def show_accounts():
    if not accounts:
        print("No accounts yet.")
        return
    print("\n--- All Accounts ---")
    for account in accounts:
        print(f"{account['name']}: ${account['balance']:.2f}")
    print("--------------------")

while True:
    print("\n1. Create account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check balance")
    print("5. Show all accounts")
    print("6. Exit")

    choice = input("Pick an option: ")

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
        print("Goodbye!")
        break
    else:
        print("Invalid option, try again.")
