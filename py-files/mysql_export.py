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

mydb = mysql.connector.connect (
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Set Cursor Object to execut SQL Queries
mycursor = mydb.cursor()

# Set variable log data to run function from log_collector.py
log_data = parse_journalctl_verbose_today_filtered()

sql_insert = "INSERT INTO ${DB_NAME} ('TIMESTAMP', 'MESSAGE', '_HOSTNAME', '_COMM', '_PID', 'PRIORITY', 'SYSLOG_IDENTIFIER', %s, %s, %s, %s, %s, %s, %s)"

values = ('TIMESTAMP', 'MESSAGE', '_HOSTNAME', '_COMM', '_PID', 'PRIORITY', 'SYSLOG_IDENTIFIER')

for value in values:
    if value:
        mycursor.executemany(sql_insert, values)
    else:
        break


# Commit Changes
mydb.commit()


# Close out 
mycursor.close()
mydb.close()