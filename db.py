import sqlite3
from datetime import datetime 

def initialize_db():
    # Connect to data base 
    conn = sqlite3.connect("bank.db")

    # Create a cursor 
    cur = conn.cursor()

    # Create a accounts table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        balance INTEGER DEFAULT 0
    )
    """)

    # CREATE transactions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        type TEXT NOT NULL,
        amount INTEGER NOT NULL,
        timestamp DATE,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    )
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_account(name, password):
    # Connect to data base 
    conn = sqlite3.connect("bank.db")

    # Create a cursor 
    cur = conn.cursor()

    # Insert the new user to the accounts 
    cur.execute(f"""
    INSERT INTO accounts (name, password) VALUES (?, ?)
    """, (name, password))

    # Commit the changes and close the connection
    conn.commit()   
    conn.close()

def check_user(name, password):
    # Connect to data base 
    conn = sqlite3.connect("bank.db")

    # Create a cursor 
    cur = conn.cursor()

    # Get the user by name and password
    cur.execute("""
    SELECT * FROM accounts WHERE name=? AND password=?
    """, (name, password))
    user = cur.fetchone()

    # Close the connection
    conn.close()
    return user


def get_acount_by_id(user_id):
    # Connect to data base
    conn = sqlite3.connect("bank.db")

    # Create a cursor
    cur = conn.cursor()

    # Get the user by id
    cur.execute("""
    SELECT * FROM accounts WHERE id=?
    """, (user_id,))

    user = cur.fetchone()
    # Close the connection
    conn.close()
    return user


def update_balance(user_id, new_balance):
    # Connect to data base
    conn = sqlite3.connect("bank.db")

    # Create a cursor
    cur = conn.cursor()

    # Update the new balance to the account table
    cur.execute("""
    UPDATE accounts SET balance=? WHERE id=?
    """, (new_balance, user_id))   

    # Commit the changes and close the connection   
    conn.commit()
    conn.close()


def save_transaction(user_id, type, amount):
    # Connect to data base 
    conn = sqlite3.connect("bank.db")

    # Create a cursor 
    cur = conn.cursor()

    # Save the transaction to the transactions table
    cur.execute("""
    INSERT INTO transactions (account_id, type, amount, timestamp) VALUES (?, ?, ?, ?)
    """, (user_id, type, amount, datetime.now().isoformat()))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def fetch_user_transactions(user_id):
    # Connect to data base
    conn = sqlite3.connect("bank.db")

    # Create a cursor
    cur = conn.cursor()

    # Get the user transaction by id
    cur.execute("""
    SELECT * FROM transactions where account_id=? ORDER BY timestamp DESC
    """, (user_id,))
    transactions = cur.fetchall()

    # Close the connection
    conn.close()
    return transactions


def update_password(user_id, new_password):
    # Connect to data base
    conn =sqlite3.connect("bank.db")

    # Create a cursor
    cur = conn.cursor()

    # Update the user password on the data base
    cur.execute("""
    UPDATE accounts SET password=? WHERE id=?
    """, (new_password, user_id))

    # Commit the changes and close the connections
    conn.commit()
    conn.close()