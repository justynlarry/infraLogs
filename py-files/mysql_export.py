import pymysql
import pandas as pd
import os
from parse_critical_logs import parse_journalctl_verbose_today_filtered, TARGET_KEYS


def critical_logs_insert():
    TABLE_NAME = "vm_critical_logs_table"
    COLUMN_MAP = {
        "TIMESTAMP": "record_time",
        "MESSAGE": "message",
        "_HOSTNAME": "hostname",
        "_COMM": "command_name",
        "_PID": "process_id",
        "PRIORITY": "priority",
        "SYSLOG_IDENTIFIER": "syslog_id",
    }

    # 3. Retrieve Log Data
    log_data = parse_journalctl_verbose_today_filtered()


    # --- SQL Insertion Logic ---
    COLUMNS_SQL = [COLUMN_MAP[key] for key in TARGET_KEYS]
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

        return sql_insert, data_to_insert
    print(f"Prepared {len(data_to_insert)} records for insertion.")

  