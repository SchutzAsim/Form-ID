from math import trunc

import mariadb
import sys


config = {
    "user": "remote",
    "password": "myremote",
    "host": "localhost",
    "port": 3306,
    "database": "Shop"
}


try:
    conn = mariadb.connect(**config)
    print("Connection Successful")

    cursor = conn.cursor(dictionary=True)
    print("Cursor created")

except mariadb.Error as e:
    print(f"Error occur in connecting to Mariadb Server with error code {e}")
    sys.exit(1)