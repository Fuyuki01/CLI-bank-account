import json
import argparse
import hashlib
from datetime import datetime
import getpass

user_accounts = "acounts.json"
balance_json = "balance.json"
user_transactions = "transactions.json"

class Account:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.user_balance = self._load_balance_from_file()
        self.user_account = self._load_accounts_from_file()
        self.user_transactions = self._load_transactions_from_file()
    
    def balance(self):
        return self.user_balance["balance"]

    def transactions(self):
        logs = []
        for transaction in self.user_transactions:
            logs.append(f"type: {transaction['type']}, amount: {transaction['amount']}, time: {transaction['timestamp']}")
        return logs
    
    def deposit(self, amount):
        try:
            self.user_balance["balance"] += int(amount)
            self.save_transaction("deposit", amount)
            print(f"${amount} added succesfully")
            print(f"current balance is ${self.user_balance['balance']}")
            self.save_balance()
        except ValueError:
            print("Invalid amount. please enter a number")
    
    def withdraw(self, amount):
        if self.user_balance["balance"] < amount:
            print("Withdraw has not been made insufficient funds")
            return
        try:
            self.user_balance["balance"] -= int(amount)
            self.save_transaction("withdraw", amount)
            print(f"${amount} withdrawn succesfully")
            print(f"current balance is ${self.user_balance['balance']}")
            self.save_balance()
        except ValueError:
            print("Invalid amount. please enter a number")

    def money_transfer(self, to, amount):
        if self.user_balance["balance"] < amount:
            print("Transfer has not been made insufficient funds")
            return

        if self.name == to:
            print("you cannot transfer money to yourself")
            return 
        
        balances = loading_balance()
        recipient_found = False
        for balance in balances:
            if balance["name"] == to:
                recipient_found = True
                balance["balance"] += int(amount)
                print(f"${amount} has been transfered succesfully to {to}")
                self.recipient_transaction(to, amount)
                break
        if not recipient_found:
            print("recipient has not been found")
            return
        
        self.user_balance["balance"] -= int(amount)
        self.save_balance()
        self.save_transaction("transfer-sent", amount)
        
        with open(balance_json, "w") as file:
            json.dump(balances, file, indent=4)

    def password_check(self, input_password):
        if self.user_account == None:
            return False
        return self.user_account["password"] == hash_password(input_password)
    
    def name_check(self, input_name):
        if self.user_account == None:
            return False
        return self.user_account["name"] == input_name

    def change_password(self, newpassword):
        self.user_account["password"] = hash_password(newpassword)
        accounts = loading_accounts()
        for account in accounts:
            if account["name"] == self.name:
                account["password"] = hash_password(newpassword)
                print("your password has been changed successfully")
                break
        with open(user_accounts, "w") as file:
            json.dump(accounts, file, indent=4)

    def save_balance(self):
        balances = loading_balance()
        for balance in balances:
            if balance["name"] == self.name:
                balance["balance"] = self.user_balance["balance"]
                break
        
        with open(balance_json, "w") as file:
            json.dump(balances, file, indent=4)

    def save_transaction(self, type, amount):
        transactions = loading_transactions()
        new_transaction = {
            "type": type,
            "amount": amount, 
            "timestamp": datetime.now().isoformat()
        }

        transactions.setdefault(self.name, []).append(new_transaction)

        with open(user_transactions, "w") as file:
            json.dump(transactions, file, indent=4)
    
    def recipient_transaction(self, to, amount):
        recipient_transactions = loading_transactions()
        recipient_transactions.setdefault(to, []).append({
            "type": "received",
            "amount": amount,
            "from": self.name,
            "timestamp": datetime.now().isoformat()
        })

        with open(user_transactions, "w") as file:
            json.dump(recipient_transactions, file, indent=4)

    def _load_balance_from_file(self):
        balances = loading_balance()
        for balance in balances:
            if balance["name"] == self.name:
                return balance 
        return {"name": self.name, "balance": 0}

    def _load_accounts_from_file(self):
        accounts = loading_accounts()
        for account in accounts:
            if account["name"] == self.name:
                return account
        return None
    
    def _load_transactions_from_file(self):
        transactions = loading_transactions()
        return transactions.get(self.name, [])


def loading_accounts():
    try:
        with open(user_accounts) as file:
            accounts = json.load(file)
        return accounts
    except FileNotFoundError:
        return []


def loading_balance():
    try:
        with open(balance_json) as file:
            balances = json.load(file)
        return balances
    except FileNotFoundError:
        return []


def loading_transactions():
    try:
        with open(user_transactions) as file:
            accounts = json.load(file)
        return accounts
    except FileNotFoundError:
        return []


def get_next_account_id(accounts):
    if not accounts:
        return 1
    return max(account["id"] for account in accounts) + 1


def hash_password(password):
    h = hashlib.sha256()
    h.update(password.encode())
    password_hash = h.hexdigest()
    return password_hash


def opening_account(name, password):
    accounts = loading_accounts()
    balances = loading_balance()
    new_account =   {
        "name": name,
        "password": hash_password(password),
        "id": get_next_account_id(accounts)
    }
    new_balance = {
        "name": name,
        "balance": 0
    }
    accounts.append(new_account)
    balances.append(new_balance)
    with open(user_accounts, "w") as file:
        json.dump(accounts, file, indent=4)
     
    with open(balance_json, "w") as file:
        json.dump(balances, file, indent=4)


def main():
    while True:
        question = input("do you have a account if you have type 1 for oppening acount 2 to leave select 0: ")
        if question in ["1", "2"]:
            break
        elif question == "0":
            return
        else:
            print("you have to select an option or to leave 0")
            
    name = input("name: ").strip().lower()
    password = getpass.getpass("password: ")
    
    if question == "1":
        user = Account(name, password)
        checked =  user.password_check(password)
    elif question == "2":
        opening_account(name, password)
        user = Account(name, password)
        print(f"Welcome to the **** bank {name}")
        print("Please login to your account with the password you have created") 
        password = getpass.getpass("password: ")
        checked = user.password_check(password)
    
    if checked:
        print(f"you have succesfully loged in {name}")
        while True:
            command = input("- ").strip().split(" ", 1)

            if not command:
                continue

            action = command[0].strip().lower()

            if action in ["clear", "exit", "quit"]:
                print("you're loging out")
                break
            elif action == "balance":
                balance = user.balance()
                print("-" * 40)
                print(f"the current balance is ${balance}")
            elif action == "transactions":
                logs = user.transactions()
                for log in logs:
                    print(log)
            elif action == "deposit":
                parse = argparse.ArgumentParser(prog="deposit", add_help=False)
                parse.add_argument("--amount", type=int, required=True, help="Amount of the depoist")
                try:
                    args = parse.parse_args(command[1].split())
                    user.deposit(args.amount)
                except:
                    print("Usage: deposit --amount 50")
            elif action == "withdraw":
                parse = argparse.ArgumentParser(prog="withdraw", add_help=False)
                parse.add_argument("--amount", type=int, required=True, help="Amount of the withdraw")
                try:
                    args = parse.parse_args(command[1].split())
                    user.withdraw(args.amount)
                except:
                    print("Ussage withdraw --amount 50")
            elif action == "change-password":
                parse = argparse.ArgumentParser(prog="new", add_help=False)
                parse.add_argument("--new", type=str, required=True, help="New password")
                try:
                    args = parse.parse_args(command[1].split())
                    password_again = getpass.getpass("please enter your old password ")
                    if hash_password(password_again) == user.user_account["password"]:
                        user.change_password(args.new)
                    else:
                        print("password is wrong")
                except:
                    print("Usage: change-password --new newpassword")
            elif action == "transfer":
                parse = argparse.ArgumentParser(prog="transfer", add_help=False)
                parse.add_argument("--to", type=str,required=True, help="to whom")
                parse.add_argument("--amount", type=int, required=True, help="the amount")
                try:
                    args = parse.parse_args(command[1].split())
                    user.money_transfer(args.to, args.amount)
                except:
                    print("Usage: transfer --to jack --amount $150")

    elif not checked:
        print("name or password wrong")


if __name__ == "__main__":
    main()
