from settings import database_table, default_balance, databasew
from db_connection import *
import os
import bcrypt

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

def hash_password(password_choice):

    password_choice.encode(encoding = 'UTF-8', errors = 'strict')

    hashword = bcrypt.hashpw(password_choice.encode('UTF-8'), bcrypt.gensalt)

    return hashword

def hash_check(myresult, password_choice):
    password_choice

def new_check(cursor, username_choice, hashword, password_choice):
    sql_query = "SELECT USERNAME, PASSWORD FROM %s WHERE USERNAME = '%s' AND PASSWORD = '%s'" % (database_table, username_choice, hashword)

    cursor.execute(sql_query)

    myresult = cursor.fetchall()
    print(myresult)

def newpw_check(cursor, hashword, password_choice):


def user_check(cursor, username_choice, password_choice):
    sql_query = "SELECT USERNAME, PASSWORD FROM %s WHERE USERNAME = '%s' AND PASSWORD = '%s'" % (database_table, username_choice, password_choice)
    
    cursor.execute(sql_query)

    myresult = cursor.fetchall()

    password_choice.encode(encoding = 'UTF-8', errors = 'strict')

    bcrypt.checkpw(password_choice.encode('UTF-8'), myresult)

    if bcrypt.checkpw(password_choice.encode('UTF-8'), myresult):
        print(myresult)
        print("LOGIN SUCCESSFUL")
        return True
    else:
        print("Username and Password did not match.")
        print(bcrypt.checkpw(password_choice.encode('UTF-8'), myresult))
        return False

def register(conn, cursor):

    reset_values()

    username_choice = input("Please input your username of choice: ")

    if not username_check(cursor, username_choice):

        print("Username was accepted!")

        password_choice = input("Please input your password: ")

        # We're going to be hashing the password here
        # Remember that the has is over 25 characters long so make
        # - sure to redo the table to take in the hashed password

        sql_query = "INSERT INTO %s(username, password, balance) VALUES ('%s', '%s', '%s')" % (database_table, username_choice, hashed_pw, default_balance)

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

    stored_hash = myresult

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