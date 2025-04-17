import json
import argparse

user_accounts = "acounts.json"
balance_json = "balance.json"

class Account:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.userbalance = self._load_balance_from_file()
        self.useraccount = self._load_accounts_from_file()
    
    def balance(self):
        return self.userbalance["balance"]
    
    def deposit(self, amount):
        try:
            self.userbalance["balance"] += int(amount)
            print(f"${amount} added succesfully")
            print(f"current balance is ${self.userbalance['balance']}")
            self.save_balance()
        except ValueError:
            print("Invalid amount. please enter a number")
    
    def withdraw(self, amount):
        try:
            self.userbalance["balance"] -= int(amount)
            print(f"${amount} withdrawn succesfully")
            print(f"current balance is ${self.userbalance['balance']}")
            self.save_balance()
        except ValueError:
            print("Invalid amount. please enter a number")
    
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

    def save_balance(self):
        balances = loading_balance()
        for balance in balances:
            if balance["name"] == self.name:
                balance["balance"] = self.userbalance["balance"]
                break
        
        with open(balance_json, "w") as file:
            json.dump(balances, file, indent=4)
    

    def password_check(self, input_password):
        if self.useraccount == None:
            return False
        return self.useraccount["password"] == input_password
    
    def name_check(self, input_name):
        if self.useraccount == None:
            return False
        return self.useraccount["name"] == input_name


def loading_accounts():
    try:
        with open(user_accounts, "r") as file:
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


def get_next_account_id(accounts):
    if not accounts:
        return 1
    return max(account["id"] for account in accounts) + 1

def opening_account(name, password):
    accounts = loading_accounts()
    balances = loading_balance()
    new_account =   {
        "name": name,
        "password": password,
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
    question = input("do you have a account if you have type 1 for oppening acount 2 ")
    name = input("name: ")
    password = input("password: ")
    
    if question == "1":
        user = Account(name, password)
        checked = user.name_check(name) and user.password_check(password)
    elif question == "2":
        opening_account(name, password)
        user = Account(name, password)
        print(f"Welcome to the **** bank {name}")
        print("Please login to your account with the password you have created") 
        password = input("password: ")
        checked = user.password_check(password)
    
    if checked:
        print(f"you have succesfully loged in {name}")
        while True:
            command = input("- ").strip().split(" ", 1)

            if not command:
                continue

            action = command[0]

            if action in ["clear", "exit", "quit"]:
                print("you're loging out")
                break
            elif action == "balance":
                balance = user.balance()
                print("-" * 40)
                print(f"the current balance is ${balance}")
            elif action == "deposit":
                parse = argparse.ArgumentParser(prog="deposit", add_help=False)
                parse.add_argument("--amount", type=int, required=True, help="Amount of the depoist")
                try:
                    args = parse.parse_args(command[1].split())
                    user.deposit(args.amount)
                except:
                    print("Ussage deposit --amount 50")
            elif action == "withdraw":
                parse = argparse.ArgumentParser(prog="withdraw", add_help=False)
                parse.add_argument("--amount", type=int, required=True, help="Amount of the depoist")
                try:
                    args = parse.parse_args(command[1].split())
                    user.withdraw(args.amount)
                except:
                    print("Ussage withdraw --amount 50")

    elif not checked:
        print("name or password wrong")


if __name__ == "__main__":
    main()
