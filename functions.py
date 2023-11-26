from settings import database_table, default_balance, databasew, database_account
from db_connection import *
import os

def draw_menu():
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print a title with some decorative characters
    print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    print("┃      Welcome to the Main Menu     ┃")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    print("              Options:               ")
    print("             1. Login                ")
    print("            2. Register              ")
    print("    3. Nothing, Work In Progress     ")
    print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

def reset_values():
    sql_query = ""
    username_choice = ""
    password_choice = ""
    return sql_query, username_choice, password_choice

def get_user_pass():
    username_choice = input("Please input your username: ")
    password_choice = input("Please input your password: ")
    return username_choice, password_choice

def login(cursor, conn):
    
    reset_values()

    username_choice = input("Please input your username: ")
    password_choice = input("Please input your password: ")

    sql_query = "SELECT * FROM %s WHERE USERNAME = '%s' AND PASSWORD = '%s'" % (database_table, username_choice, password_choice)

    cursor.execute(sql_query)

    reset_values()

    userID = cursor.fetchone()
    IDz = userID[1]

    role = userID[3]

    if userID:
        if role == 'customer':
            print("This is a customer")
            display_menu(userID, cursor, conn)
        elif role == 'employee':
            print("This is an employee")
            main_menu(cursor)
        elif role == 'admin':
            print("This is an admin.")
            main_menu(cursor)
        print("true")
    else:
        print("Username and Password not matching anything in the system please try again!")
        print("false")

def register(conn, cursor):

    reset_values()

    username_choice = input("Please input your username of choice: ")

    if not username_check(cursor, username_choice):
        print("Username was accepted!")

        password_choice = input("Please input your password: ")

        sql_query = "INSERT INTO %s(username, password) VALUES ('%s', '%s')" % (database_table, username_choice, password_choice)

        cursor.execute(sql_query)

        reset_values()
        
        conn.commit()

        print("Username and Password has been recorded to the database!")

    else:
        print("Username is already being used. Please try again.")

        register()

def get_balance(userID, cursor):
    query = "SELECT Balance FROM Account WHERE AccountID = %s" % (userID[0])
    cursor.execute(query)
    balance = cursor.fetchone()
    return balance[0] if balance else None

def display_menu(userID, cursor, conn):
    while True:
                balance = get_balance(userID, cursor)
                print(f"Welcome {userID[3]}, {userID[1]}!")
                print(f"Balance: {balance}")

                print("\n1. Deposit")
                print("2. Withdraw")
                print("3. Logout")

                choice = input("Enter your choice (1-3): ")

                if choice == "1":
                    amount = float(input("Enter the deposit amount: $"))
                    deposit(userID, amount, cursor, conn)

                elif choice == "2":
                    amount = float(input("Enter the withdrawal amount: $"))
                    withdraw(userID, amount, cursor, conn)

                elif choice == "3":
                    print("Logout successful. Goodbye!")
                    break

                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")

def withdraw(userID, amount, cursor, conn):
    balance = get_balance(userID, cursor)
    if balance <= 0:
        print("You cannot withdraw any more money.")
    else:
        subtracted_balance = balance - amount

        query = "UPDATE Account SET Balance = %s WHERE AccountID = %s" % (subtracted_balance, userID[0])

        cursor.execute(query)

        if cursor.rowcount > 0:
            conn.commit()

            print(f"Withdrew ${amount} from AccountID {userID[1]}.")

        else:
            print("Insufficient funds or invalid AccountID.")

def deposit(userID, amount, cursor, conn):
    balance = get_balance(userID, cursor)
    added_balance = balance + amount
    query = "UPDATE Account SET Balance = %s WHERE AccountID = %s" % (added_balance, userID[0])
    cursor.execute(query)
    conn.commit()
    print(f"Deposited ${amount} to AccountID {userID}.")

def username_check(cursor, username_choice):
    sql_query = "SELECT USERNAME FROM %s WHERE USERNAME = '%s'" % (database_table, username_choice)
    
    cursor.execute(sql_query)

    myresult = cursor.fetchall()

    if myresult:
        return True
    else:
        print("Username was not found in the database!")
        return False

def password_check(cursor, username_choice):
    sql_query = "SELECT PASSWORD FROM %s WHERE USERNAME = '%s'" % (database_table, username_choice)
    
    cursor.execute(sql_query)

    myresult = cursor.fetchall()

    if myresult:
        return True
    else:
        print("Password was not found in the database!")
        return False

def databaseErrorMenu():

    while True:
        print("************************************************")
        print("    Welcome to the Database Creation Wizard    ")
        print("************************************************")
        print("Warning: You are about to create a new database.")

        choice = input("Do you want to continue? (Y/n): ").strip().lower()

        if choice == "yes":
            #print("\nDatabase created successfully!\n")
            return True
        elif choice == "no":
            print("\nDatabase creation canceled. Exiting program.\n")
            return False


def display_account_menu():
    print("\n=== MENU ===")
    print("1. View all accounts")
    print("2. View accounts by Account Type")
    print("3. View accounts by Customer ID")
    print("4. Exit")

def view_all_accounts(cursor):
    cursor.execute("SELECT * FROM Account")
    accounts = cursor.fetchall()
    if accounts:
        print("\n=== All Accounts ===")
        for account in accounts:
            print(account)
    else:
        print("No accounts found.")

def view_accounts_by_type(cursor):
    account_type = input("Enter Account Type: ")
    cursor.execute("SELECT * FROM Account WHERE AccountType = ?", (account_type,))
    accounts = cursor.fetchall()
    if accounts:
        print(f"\n=== Accounts with Account Type '{account_type}' ===")
        for account in accounts:
            print(account)
    else:
        print(f"No accounts found with Account Type '{account_type}'.")

def view_accounts_by_customer_id(cursor):
    customer_id = input("Enter Customer ID: ")
    cursor.execute("SELECT * FROM Account WHERE CustomerID = ?", (customer_id,))
    accounts = cursor.fetchall()
    if accounts:
        print(f"\n=== Accounts for Customer ID '{customer_id}' ===")
        for account in accounts:
            print(account)
    else:
        print(f"No accounts found for Customer ID '{customer_id}'.")

def view_all_customers(cursor):
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    if customers:
        print("\n=== All Customers ===")
        for customer in customers:
            print(customer)
    else:
        print("No customers found.")

# Function to find customer by ID
def find_customer_by_id(cursor):
    customer_id = input("Enter Customer ID: ")
    cursor.execute("SELECT * FROM Customer WHERE CustomerID = ?", (customer_id,))
    customer = cursor.fetchone()
    if customer:
        print(f"\n=== Customer with ID '{customer_id}' ===")
        print(customer)
    else:
        print(f"No customer found with ID '{customer_id}'.")

# Function to find customer by Name
def find_customer_by_name(cursor):
    name = input("Enter Customer Name: ")
    cursor.execute("SELECT * FROM Customer WHERE Name = ?", (name,))
    customers = cursor.fetchall()
    if customers:
        print(f"\n=== Customers with Name '{name}' ===")
        for customer in customers:
            print(customer)
    else:
        print(f"No customers found with Name '{name}'.")

def display_customer_menu():
    print("\n=== MENU ===")
    print("1. View all customers")
    print("2. Find customer by ID")
    print("3. Find customer by Name")
    print("4. Exit")


# Function to view all transactions
def view_all_transactions(cursor):
    print("You've chosen to view all transactions.")
    print("\nStep 1: Fetching all transactions...")
    cursor.execute("SELECT * FROM Transaction")
    transactions = cursor.fetchall()
    if transactions:
        print("\nStep 2: Displaying all transactions")
        print("\n=== All Transactions ===")
        for transaction in transactions:
            print(transaction)
    else:
        print("\nStep 2: No transactions found.")


# Function to find transactions by Account ID
def find_transactions_by_account_id(cursor):
    print("You've chosen to find transactions by Account ID.")
    account_id = input("Enter Account ID: ")
    print(f"\nStep 1: Searching for transactions with Account ID '{account_id}'...")
    cursor.execute("SELECT * FROM Transaction WHERE AccountID = ?", (account_id,))
    transactions = cursor.fetchall()
    if transactions:
        print(f"\nStep 2: Displaying transactions for Account ID '{account_id}'")
        print(f"\n=== Transactions for Account ID '{account_id}' ===")
        for transaction in transactions:
            print(transaction)
    else:
        print(f"\nStep 2: No transactions found for Account ID '{account_id}'.")



def display_transactions_menu():
    print("\n=== MENU ===")
    print("1. View all transactions")
    print("2. Find transactions by Account ID")
    print("3. Exit")


def main_menu(cursor):
    while True:
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\033[1;33m")  # Bold and yellow color
        print("=== STAFF MAIN MENU ===")
        print("\033[0;36m")  # Cyan color
        print("1. \033[1;36mAccount Menu\033[0;36m")
        print("2. \033[1;36mCustomer Menu\033[0;36m")
        print("3. \033[1;36mTransactions Menu\033[0;36m")
        print("4. \033[1;36mExit\033[0m")  # Reset to default color
        print("\033[0m")  # Reset formatting

        choice = input("Enter your choice: ")

        if choice == "1":
            display_account_menu(cursor)
        elif choice == "2":
            display_customer_menu(cursor)
        elif choice == "3":
            display_transactions_menu(cursor)
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def display_account_menu(cursor):
    while True:

        print("\n=== ACCOUNT MENU ===")
        print("1: View All Accounts")
        print("2: View Accounts by Type")
        print("3: View Accounts by Customer ID")
        print("4: Break out")
        # ...
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_accounts(cursor)
        elif choice == "2":
            view_accounts_by_type(cursor)
        elif choice == "3":
            view_accounts_by_customer_id(cursor)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def display_customer_menu(cursor):
    while True:
        print("\n=== CUSTOMER MENU ===")
        print("1: View All Customers")
        print("2: Find Customer By ID")
        print("3: Find Customer by Name")
        print("4: Break out")
        # ...
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_customers(cursor)
        elif choice == "2":
            find_customer_by_id(cursor)
        elif choice == "3":
            find_customer_by_name(cursor)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

def display_transactions_menu(cursor):
    while True:

        print("\n=== TRANSACTIONS MENU ===")
        print("1: View All Transactions")
        print("2: Find Transactions By Account ID")
        print("3: Break Out")
        # ...
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_transactions(cursor)
        elif choice == "2":
            find_transactions_by_account_id(cursor)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

# Other existing function definitions remain the same