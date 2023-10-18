import mysql.connector
import socket
from functions import databaseErrorMenu
from settings import database_table

def is_server_online(host, port):
    try:
        # Create a socket to the MySQL server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Adjust the timeout as needed

        # Try to connect to the server
        sock.connect((host, port))
        sock.close()
        return True
    except Exception as e:
        return False

def initial_connection(db_config):
    try:
        # Attempt to connect to the MySQL server
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as err:
        return None, None

def connect_to_database(db_config, create_if_not_exists=False):
    if is_server_online(db_config['host'], db_config.get('port', 3306)):
        conn, cursor = initial_connection(db_config)
        if conn and cursor:
            return conn, cursor
        else:
            if create_if_not_exists:
                print("Database connection failed. Attempting to create the database.")
                try:
                    if databaseErrorMenu():
                        # Try to create the database
                        conn = mysql.connector.connect(
                            host=db_config['host'],
                            user=db_config['user'],
                            password=db_config['password']
                        )
                        cursor = conn.cursor()
                        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']};")
                        cursor.execute(f"Use {db_config['database']};")
                        execute(cursor)
                        conn.commit()
                        conn.close()
                        print("Database created successfully.")
                except mysql.connector.Error as err:
                    print(f"Error creating database: {err}")
            else:
                print("Database connection failed.")
    else:
        print("Server is not running. Please check the settings and make sure you've inputted the correct information.")

    return None, None

def execute(cursor):
    cursor.execute(f"CREATE TABLE {database_table}(stdId int PRIMARY KEY Auto_Increment, username varchar(25), password varchar(25), balance int);")
    print("Table Created!")
    return