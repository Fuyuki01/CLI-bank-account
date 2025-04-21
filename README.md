# CLI Bank App

A simple command-line banking system written in Python using Sqlite, built as a project to practice and learn Object-Oriented Programming

---

## Features

- Create new bank accounts
- Secure login with password hashing
- Deposit, withdraw, and transfer funds
- View transaction history
- All data is saved persistently in a SQLite database (`bank.db`)
- CLI interface using `argparse`
  
---
### Clone the repository
```bash
git clone https://github.com/Fuyuki01/CLI-bank-account.git
cd Cli-bank-account
```
---

## Running The Program
```bash
python bankapp.py  
```
---

## Usage

### Logging In
When prompted:
```
Do you have an account? (1 for yes, 2 to open one, 0 to exit): 
```

Choose `1` to log in or `2` to register a new account to leave press 0 .

---

### Command Options (after login)

#### View Balance
```
balance
```
**Output:**
```
Your current balance is $100
```

#### Deposit Money
```
deposit --amount <value>
```
**Output:**
```
$50 added successfully
Current balance is $150
```

### Viewing Transactions
```
transactions
```
**Output:**
```
<type> | $<amount> | <time> 
```

#### Withdraw Money
```
withdraw --amount <value>
```
**Output:**
```
$20 withdrawn successfully
Current balance is $130
```

#### Transfer Money
```
transfer --to <user> --amount <value>
```
**Output:**
```
$50 has been succesfully transfered to <user> 
```

#### Change Password
```
change-password --new <newpassword>
```
**Output:**
```
password changed successfully 
```

#### Logout / Exit
```
clear
exit
quit
```

---

## Project Files

- `bankapp.py` — main application file
- `db.py` - handles all database queries and interactions
- `bank.db` — SQLite database storing account information and transaction history
  
---
