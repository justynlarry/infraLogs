import mysql.connector
import os
from log_collector import parse_journalctl_verbose_today_filtered
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("MYSQL_HOST")
DB_USER = os.environ.get("MYSQL_USER")
DB_PASSWORD= os.environ.get("MYSQL_PASSWORD")
DB_NAME = os.environ.get("MYSQL_DATABASE")
TABLE_NAME = "log_table"

# --- Database Connection and Setup ---
try:
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        # 1.  Establish Connection
        mydb = mysql.connector.connect (
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        # 2. Set Cursor Object to execute SQL Queries
        mycursor = mydb.cursor()

except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
    # Exit gracefully if connection fails
    exit(1)
except ValueError as err:
    print(f"Configuration Error: {err}")
    exit(1)

# 3. Retrieve Log Data
log_data = parse_journalctl_verbose_today_filtered()

if not log_data:
    print("No log data to insert. Exiting.")
    mycursor.close()
    mydb.close()
    exit(0)

# --- SQL Insertion Logic ---
COLUMNS_SQL = [f'`{col}`' if col == 'TIMESTAMP' else col for col in TARGET_KEYS]
COLUMN_NAMES_STR = ", ".join(COLUMNS_SQL)
PLACEHOLDERS_STR = ", ".join(["%s"] * len(TARGET_KEYS))


sql_insert = (
    f"INSERT INTO {TABLE_NAME} ({COLUMN_NAMES_STR}) "
    f"VALUES ({PLACEHOLDERS_STR})"
)
print(f"Generated SQL Template: {sql_insert}")

# --- Dataq Preparation for executemany ---
data_to_insert = []
for record in log_data:
    row_tuple = tuple(record.get(key) for key in TARGET_KEYS)
    data_to_insert.append(row_tuple)

print(f"Prepared {len(data_to_insert)} records for insertion.")

# --- Execution ---
try:
    mycursor.executemany(sql_insert, data_to_insert)
    mydb.commit()

    print(f"Successfully inserted {mycursor.rowcount} records into the database.")

except mysql.connector.Error as err:
    print(f"SQL Insertion Error: {err}")
    mydb.rollback()

finally:
# Close out 
    mycursor.close()
    mydb.close()
    print("Database connection closed.")