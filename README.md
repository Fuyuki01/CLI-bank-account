# CLI Bank App

A simple command-line banking system written in Python, built as a project to practice and learn Object-Oriented Programming

---

## Features

- Create new bank accounts
- Log in to existing accounts
- Deposit and withdraw money, and transfer money
- Check current balance and transaction history
- Data saved to JSON files (`accounts.json`, `balance.json`)
- Command-line interface using `argparse`

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

Choose `1` to log in or `2` to register a new account or press 0 to exit.

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

#### View Transactions
```
transactions
```
**Output:**
```
type: <type>, amount: <amount>, time: <timestamp>
```

#### Deposit Money
```
deposit --amount 50
```
**Output:**
```
$50 added successfully
Current balance is $150
```

#### Withdraw Money
```
withdraw --amount 20
```
**Output:**
```
$20 withdrawn successfully
Current balance is $130
```

#### Transfer Money
```
transfer --to <user>  --amount 20
```
**Output:**
```
$<amount> has been transferred successfully to <user> 
```

#### Change Password
```
change-password --new <newpassword>
```
**Output:**
```
password has been changed successfully 
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
- `accounts.json` — stores usernames and passwords  
- `balance.json` — stores account balances
- `transactions.json` - stores transaction history
- 
---
