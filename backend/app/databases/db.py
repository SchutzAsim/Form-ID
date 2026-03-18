import os
import mariadb
import sys
from dotenv import load_dotenv

load_dotenv()

config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT")),
    "database": os.getenv("DB_DATABASE"),
    "unix_socket": None
}


try:
    conn = mariadb.connect(**config)
    print("Connection Successful")

    cursor = conn.cursor(dictionary=True)
    print("Cursor created")

except mariadb.Error as e:
    print(f"Error occur in connecting to Mariadb Server with error code {e}")
    sys.exit(1)