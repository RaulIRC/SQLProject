import mysql.connector
import socket
from functions import databaseErrorMenu
from settings import database_table, mydb_config

def is_server_online(host: str, port: str):
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

def initial_connection(mydb_config: dict [str, ]):
    try:
        # Attempt to connect to the MySQL server
        conn = mysql.connector.connect(**mydb_config)
        cursor = conn.cursor()
        return conn, cursor
    except mysql.connector.Error as err:
        return None, None

def connect_to_database(mydb_config: dict[str, ], create_if_not_exists=False):
    if is_server_online(mydb_config['host'], mydb_config.get('port', 3306)):
        conn, cursor = initial_connection(mydb_config)
        if conn and cursor:
            return conn, cursor
        else:
            if create_if_not_exists:
                print("Database connection failed. Attempting to create the database.")
                try:
                    if databaseErrorMenu():
                        # Try to create the database
                        conn = mysql.connector.connect(
                            host=mydb_config['host'],
                            user=mydb_config['user'],
                            password=mydb_config['password']
                        )
                        cursor = conn.cursor()
                        databaseCreation(cursor, mydb_config)
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

def databaseCreation(cursor, mydb_config):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {mydb_config['database']};")
    cursor.execute(f"Use {mydb_config['database']};")
    cursor.execute(f"CREATE TABLE {database_table}(stdId int PRIMARY KEY Auto_Increment, username varchar(25), password varchar(50), balance int);")
    print("Table Created!")