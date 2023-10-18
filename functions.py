from settings import database_table, default_balance, databasew
from db_connection import *
import os

def draw_menu():
    print("|    Select from the options below!    |")
    print("|             1 : Login                |")
    print("|            2 : Register              |")
    print("|        3 : Work-In-Progress          |")

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

# This password check function is being used for the login function to check if it matches the one in the system.
# I just made it because I needed to see if I could get both values.

def reset_values():
    username_choice = ""
    password_choice = ""
    return username_choice, password_choice

def user_check(cursor, username_choice, password_choice):
    sql_query = "SELECT USERNAME, PASSWORD FROM %s WHERE USERNAME = '%s' AND PASSWORD = '%s'" % (database_table, username_choice, password_choice)
    
    cursor.execute(sql_query)

    myresult = cursor.fetchall()

    if myresult:
        print(myresult)
        return True
    else:
        print("Username and Password did not match.")
        return False

def register(conn, cursor):

    reset_values()

    username_choice = input("Please input your username of choice: ")

    if not username_check(username_choice):

        print("Username was accepted!")

        password_choice = input("Please input your password: ")

        sql_query = "INSERT INTO %s(username, password, balance) VALUES ('%s', '%s', '%s')" % (database_table, username_choice, password_choice, default_balance)

        cursor.execute(sql_query)

        reset_values()
        
        conn.commit()

        print("Username and Password has been recorded to the database!")

    else:
        print("Username is already being used. Please try again.")

        register()

def username_check(cursor, username_choice):
    sql_query = "SELECT USERNAME FROM %s WHERE USERNAME = '%s'" % (database_table, username_choice)
    #variables = database_table, username_choice
    cursor.execute(sql_query)

    myresult = cursor.fetchall()

    if myresult:
        print(myresult)
        return True
    else:
        print("Username was not found in the database!")
        return False

def password_check(cursor, username_choice):
    sql_query = "SELECT PASSWORD FROM %s WHERE USERNAME = '%s'" % (database_table, username_choice)
    #variables = database_table, username_choice
    cursor.execute(sql_query)

    myresult = cursor.fetchall()

    if myresult:
        print(myresult)
        return True
    else:
        print("Password was not found in the database!")
        return False

def login(cursor):
    reset_values()

    username_choice = input("Please input your username: ")

    password_choice = input("Please input your password: ")

    # Just testing a new function for the system.
    if not user_check(cursor, username_choice, password_choice):
        print("ERROR: USERNAME AND PASSWORD ARE NOT FOUND")
    else:
        print(username_choice, password_choice)
        print("CORRECT INFORMATION LOGGING IN")

def databaseCreate(cursor):
    sql_query = "CREATE DATABASE IF NOT EXISTS '%s'" % (databasew)
    cursor.execute(sql_query)

    myresult = cursor.fetchall()

    print(myresult)
    print("DATABASE HAS BEEN CREATED LETS GOOO")

def databaseErrorMenu():
    print("************************************************")
    print("    Welcome to the Database Creation Wizard    ")
    print("************************************************")
    print("Warning: You are about to create a new database.")
    
    while True:
        choice = input("Do you want to continue? (Y/n): ").strip().lower()
    
        if choice == "yes":
            #print("\nDatabase created successfully!\n")
            return True
        elif choice == "no":
            print("\nDatabase creation canceled. Exiting program.\n")
            return False
        else:
            print("Invalid choice. Please enter 'yes' or 'no.'")