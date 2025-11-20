import pymysql, os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("MYSQL_HOST")
DB_USER = os.environ.get("MYSQL_USER")
DB_PASSWORD= os.environ.get("MYSQL_PASSWORD")
DB_NAME = os.environ.get("MYSQL_DATABASE")
DB_PORT = os.environ.get("MYSQL_PORT", 3306)

def get_db(): 
    return pymysql.connect (
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=int(DB_PORT),
    )

def insert_records(table_name, column_names, row_data_list):
    """
    Inserts multiple rows into MySQL
    column_names = [col1, col2, ...]
    row_data_list = [(val1,val2,...), (...), ...]
    """

    if not row_data_list:
            print("No records to insert.")
            return

    placeholder = ", ".join(["%s"] * len(column_names))
    col_str = ", ".join(column_names)

    sql = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholder}) ON DUPLICATE KEY UPDATE message=VALUES(message)"

    db = get_db()
    cur = db.cursor()

    try:
        cur.executemany(sql, row_data_list)
        db.commit()
        print(f"Inserted {cur.rowcount} rows.")
    except Exception as e:
        print("DB insert failed:", e)
        db.rollback()
    finally:
        cur.close()
        db.close()