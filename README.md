# Elite 102 - Banking App

A terminal-based banking system built with Python and MySQL for the Elite 102 course.

## Features

- Create bank accounts with a starting balance
- Deposit and withdraw money (prevents negative balances)
- Transfer money between accounts
- Delete accounts (requires zero balance + confirmation)
- Check individual account balances
- View all accounts with total balance
- Transaction history with timestamps
- Input validation on all operations
- Startup connection check
- Data saved permanently using MySQL

## Files

| File | Description |
|------|-------------|
| `bank.py` | Simple version using in-memory storage (no database needed) |
| `bank_mysql.py` | Full version connected to MySQL with transaction logging |
| `bank_db.sql` | SQL script to set up the database and tables in MySQL Workbench |
| `run_bank.bat` | Double-click launcher for Windows |

## Setup

### 1. Install Requirements

- Python 3
- MySQL Server
- MySQL Workbench
- mysql-connector-python (`pip install mysql-connector-python`)

### 2. Create the Database

Open MySQL Workbench, load `bank_db.sql`, and run it. This creates:

- `banking_system` database
- `accounts` table (name, balance)
- `transactions` table (type, amount, timestamp)

### 3. Configure Password

In `bank_mysql.py`, update the password on line 7 to match your MySQL root password.

### 4. Run

Double-click `run_bank.bat` or run from terminal:

```
python bank_mysql.py
```

## Menu

```
===== Banking System =====
1. Create Account
2. Deposit
3. Withdraw
4. Transfer Money
5. Check Balance
6. All Accounts
7. Transaction History
8. Delete Account
9. Exit
```

## Built With

- Python 3
- MySQL
- MySQL Workbench
