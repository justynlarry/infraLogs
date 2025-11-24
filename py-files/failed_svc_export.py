import os
from parse_failed_svc import parse_failed_svc, TARGET_KEYS
from mysql_export import insert_records
from datetime import datetime

TABLE_NAME = "failed_svcs"

COLUMN_MAPPING = {
    'UNIT':         'unit',
    'LOAD':         'load',
    'ACTIVE':       'active',
    'SUB':          'sub',
    'DESCRIPTION':  'description',
    'REPORT_HOST':  'report_host',
    'REPORT_DATE':  'report_date',
    'REPORT_UUID':  'report_uuid'
}

DB_COLUMNS = [
    "unit",
    "load",
    "active",
    "sub",
    "description",
    "report_host",
    "report_date",
    "report_uuid"
]

def main():
    
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"../../vm_system_reports/vm_system_report_{today}.log"

    records = parse_failed_svc(filename)

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