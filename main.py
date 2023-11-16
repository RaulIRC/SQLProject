from db_connection import connect_to_database
from settings import mydb_config
from functions import *


# Connect to the database
conn, cursor = connect_to_database(mydb_config, create_if_not_exists = True)

def choice_function(choice):
    if choice == "1":
        print("You selected Option 1")
        login(cursor)
    elif choice == "2":
        print("You selected Option 2")
        #register(conn, cursor)
    elif choice == "3":
        print("You selected Option 3")
        main_menu(cursor)
        return
    elif choice == "q":
        print("Quitting the program.")
    else:
        print("Invalid choice. Please select a valid option.")
        mainmenu()

def mainmenu():
    choice_sel = ""

    draw_menu()
    choice_sel = input("Select from the options above\nOr input 'q' to quit the program: ")
    choice_function(choice_sel)

# Main Running function inside the if statement

if conn and cursor:
    # Your database code here
    print("Server is currently up and running!!!")

    mainmenu()

    # Don't forget to close the connection when you're done
    cursor.close()
    conn.close()