
### SETTINGS FOR THE VARIABLES THAT CHANGE ###

### DATABASE CONNECTION VARIABLE ###

hostw = "localhost"
userw = "root"
passwordw = "root"
databasew = "BankDB"
portw = 3306

### DO NOT TOUCH ANYTHIGN BELOW ONLY WHAT'S ABOVE ###

### TABLE NAMES ###

database_table = "USERS"

database_account = "ACCOUNTS"

### PARAMETERS ###

# MySQL server connection parameters
mydb_config: dict[str, ] = {
    'host': hostw,
    'user': userw,
    'password': passwordw,
    'database': databasew,
    'port': portw,
}

### VARIABLES ###

default_balance = 0
