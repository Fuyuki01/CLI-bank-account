import argparse
import hashlib
from datetime import datetime
import getpass
import db

class Account:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_account = db.get_acount_by_id(user_id)
        self.name = self.user_account[1]
        self.user_balance = self.user_account[3]
        self.user_transactions = db.fetch_user_transactions(self.user_id)
    
    def balance(self):
        return self.user_balance["balance"]

    def transactions(self):
        logs = []
        for transaction in self.user_transactions:
            logs.append(f"type: {transaction[2]}, amount: {transaction[3]}, time: {transaction[4]}")
        return logs
    
    def deposit(self, amount):
        try:
            self.user_balance += int(amount)

            print(f"${amount} added succesfully")
            print(f"current balance is ${self.user_balance}")

            # Update the balance on the data base 
            db.update_balance(self.user_id, self.user_balance)
            
            # Update the transactions on the data base
            db.save_transaction(self.user_id, "deposit", amount)
        except ValueError:
            print("Invalid amount. please enter a number")
    
    def withdraw(self, amount):
        if self.user_balance < amount:
            print("Withdraw has not been made insufficient funds")
            return
        try:
            self.user_balance["balance"] -= int(amount)

            print(f"${amount} withdrawn succesfully")
            print(f"current balance is ${self.user_balance}")

            # Update the balance on the data base 
            db.update_balance(self.user_id, self.user_balance)
            
            # Update the transactions on the data base
            db.save_transaction(self.user_id, "deposit", amount)

        except ValueError:
            print("Invalid amount. please enter a number")

    def money_transfer(self, to, amount):
        if self.user_balance < amount:
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


def hash_password(password):
    h = hashlib.sha256()
    h.update(password.encode())
    password_hash = h.hexdigest()
    return password_hash


def opening_account(name, password):
    hashed_pw = hash_password(password)
    db.create_account(name, hashed_pw)


def main():
    question = input("do you have a account if you have type 1 for oppening acount 2 ")
    name = input("name: ").strip().lower()
    password = getpass.getpass("password: ")
    
    if question == "1":
        user_data = db.check_user(name, hash_password(password))
        if user_data:
            user = Account(user_data[0])
            checked = True
        else:
            checked = False
    elif question == "2":
        opening_account(name, password)
        user = Account(name, password)
        print(f"Welcome to the **** bank {name}")
        checked = True
    
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
