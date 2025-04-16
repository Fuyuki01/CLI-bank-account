# CLI Bank App

A simple command-line banking system written in Python, built as a project to practice and learn Object-Oriented Programming

---

## Features

- Create new bank accounts
- Log in to existing accounts
- Deposit and withdraw money
- Check current balance
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
Do you have an account? (1 = yes, 2 = open one): 
```

Choose `1` to log in or `2` to register a new account.

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

#### Logout / Exit
```
clear
exit
quit
```

---

## 📁 Project Files

- `bankapp.py` — main application file  
- `accounts.json` — stores usernames and passwords  
- `balance.json` — stores account balances  

---
