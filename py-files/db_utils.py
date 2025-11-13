import pymysql, os
from mysql_export import critical_logs_insert
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("MYSQL_HOST")
DB_USER = os.environ.get("MYSQL_USER")
DB_PASSWORD= os.environ.get("MYSQL_PASSWORD")
DB_NAME = os.environ.get("MYSQL_DATABASE")
DB_PORT = os.environ.get("MYSQL_PORT", 3306)

mydb = None
mycursor = None
connection_successful = False

# --- Database Connection and Setup ---
try:
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
       raise ValueError("Missing one or more required environment variables for MySQL connection.")

        # 1.  Establish Connection
    mydb = pymysql.connect (
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=int(DB_PORT),
    )
    # 2. Set Cursor Object to execute SQL Queries
    mycursor = mydb.cursor()
    print("mySQL connection established successfully.")
    connection_successful = True

except pymysql.MySQLError as err:
    print(f"Database Connection Error: {err}")
    # Exit gracefully if connection fails
    exit(1)
except ValueError as err:
    print(f"Configuration Error: {err}")
    exit(1)

if not connection_successful:
    print("FATAL: Skipping data insertion due to connection or configuration error.")
    exit(1)

sql_insert, data_to_insert = critical_logs_insert()

if not log_data:
    print("No log data to insert. Exiting.")
    mycursor.close()
    mydb.close()
    exit(0)

  # --- Execution ---
    try:
        mycursor.executemany(sql_insert, data_to_insert)
        mydb.commit()

        print(f"Successfully inserted {mycursor.rowcount} records into the database.")

    except pymysql.MySQLError as err:
        print(f"SQL Insertion Error: {err}")
        if mydb:
            mydb.rollback()

    finally:
    # Close out 
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()
        print("Database connection closed.")