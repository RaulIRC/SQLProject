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
    multiDatabaseCreation(cursor)
    databasePopulation(cursor)
    print("Tables Created!")

def multiDatabaseCreation(cursor):
    cursor.execute(f"CREATE TABLE Customer ( CustomerID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(25) NOT NULL, Address VARCHAR(50), Phone VARCHAR(25), Email VARCHAR(50), DateOfBirth DATE);")
    cursor.execute(f"CREATE TABLE Account ( AccountID INT AUTO_INCREMENT PRIMARY KEY, CustomerID INT, AccountType VARCHAR(50) NOT NULL, Balance DECIMAL(10, 2) NOT NULL, DateOpened DATE NOT NULL, Status VARCHAR(50) NOT NULL, FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID));")
    cursor.execute(f"CREATE TABLE Transaction ( TransactionID INT AUTO_INCREMENT PRIMARY KEY, AccountID INT, Date DATE NOT NULL, Amount DECIMAL(10, 2) NOT NULL, Type VARCHAR(50) NOT NULL, Description TEXT, FOREIGN KEY (AccountID) REFERENCES Account(AccountID));")

def databasePopulation(cursor):
    cursor.execute(f"INSERT INTO Customer (Name, Address, Phone, Email, DateOfBirth) VALUES ('John Doe', '123 Main St', '832-555-1010', 'johndoe@example.com', '1980-01-01'),('Jane Smith', '456 Elm St', '832-555-2020', 'janesmith@example.com', '1990-02-02'),('Alice Johnson', '789 Oak St', '832-555-3030', 'alicejohnson@example.com', '1985-03-03'),('Brian Brown', '321 Pine St', '832-555-4040', 'brianbrown@example.com', '1975-04-04'),('Olivia White', '654 Maple St', '832-555-5050', 'oliviawhite@example.com', '2000-05-05'),('Ethan Harris', '987 Cedar St', '832-555-6060', 'ethanharris@example.com', '1995-06-06'),('Sophia Davis', '159 Birch St', '832-555-7070', 'sophiadavis@example.com', '1988-07-07'),('Liam Wilson', '753 Spruce St', '832-555-8080', 'liamwilson@example.com', '1992-08-08'),('Emily Miller', '369 Willow St', '832-555-9090', 'emilymiller@example.com', '1978-09-09'),('David Taylor', '246 Alder St', '832-555-1011', 'davidtaylor@example.com', '1983-10-10');")
    cursor.execute(f"INSERT INTO Account (CustomerID, AccountType, Balance, DateOpened, Status) VALUES(1, 'Checking', 1000.00, '2022-01-01', 'Active'),(1, 'Savings', 5000.00, '2022-01-15', 'Active'),(2, 'Checking', 1500.00, '2022-02-01', 'Active'),(3, 'Savings', 3000.00, '2022-03-01', 'Active'),(4, 'Checking', 2000.00, '2022-01-01', 'Active'),(5, 'Savings', 6000.00, '2022-01-15', 'Active'),(6, 'Checking', 2500.00, '2022-02-01', 'Active'),(7, 'Savings', 3500.00, '2022-03-01', 'Active'),(8, 'Checking', 2200.00, '2022-01-01', 'Inactive'),(9, 'Savings', 5500.00, '2022-01-15', 'Active'),(10, 'Checking', 1700.00, '2022-02-01', 'Active');")
    cursor.execute(f"INSERT INTO Transaction (AccountID, Date, Amount, Type, Description) VALUES(1, '2022-02-01', 200.00, 'Deposit', 'Paycheck deposit'),(2, '2022-02-10', 50.00, 'Withdrawal', 'ATM withdrawal'),(3, '2022-03-01', 100.00, 'Deposit', 'Gift received'),(4, '2022-04-01', 200.00, 'Withdrawal', 'Online purchase'),(5, '2022-05-01', 500.00, 'Deposit', 'Tax refund'),(6, '2022-06-01', 150.00, 'Withdrawal', 'Grocery shopping'),(7, '2022-07-01', 250.00, 'Deposit', 'Freelance payment'),(8, '2022-08-01', 300.00, 'Withdrawal', 'Car repair'),(9, '2022-09-01', 400.00, 'Deposit', 'Bonus'),(10, '2022-10-01', 100.00, 'Withdrawal', 'Utility bill'),(11, '2022-11-01', 350.00, 'Deposit', 'Investment return');")