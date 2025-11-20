import os
from parse_storage import parse_storage, TARGET_KEYS
from mysql_export import insert_records
from datetime import datetime

TABLE_NAME = "storage_logs"

COLUMN_MAPPING = {
    'FILE_SYSTEM':      'filesystem',
    'SIZE':             'size',
    'USED':             'used',
    'AVAIL':            'avail',
    'USE_PERCENTAGE':   'use_percentage',
    'MOUNTED_ON':       'mounted_on'
}

DB_COLUMNS = [
    "filesystem",
    "size",
    "used",
    "avail",
    "use_percentage",
    "mounted_on"
    "report_host",
    "report_date",
    "report_uuid"
]

def main():

    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"../../vm_system_reports/vm_system_report_{today}.log"

    records = parse_storage(filename)

    print(f"Parsed {len(records)} structured log entries.")

    rows = []
    for rec in records:
        row = tuple(
            rec.get(parsed_key)
            for parsed_key in TARGET_KEYS + ["REPORT_HOST", "REPORT_DATE", "REPORT_UUID"]
        )
        rows.append(row)

    insert_records(TABLE_NAME, DB_COLUMNS, rows)

if __name__ == "__main__":
    main()