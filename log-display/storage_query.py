import pandas as pd
from mysql_import import get_db_connection

def get_storage_data():
    """
    Fetch Storage data from MySQL infralogDb01 -> table: storage_logs
    """
    try:
        conn = get_db_connection()

        query = f"""
            SELECT report_host, use_percentage, mounted_on
            FROM storage_logs
            WHERE report_date = CURDATE()
            ORDER BY report_host, mounted_on
        """
    
        df = pd.read_sql(query, conn)
        conn.close()

        return df
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()