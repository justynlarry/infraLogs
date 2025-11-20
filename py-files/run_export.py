import os
from parse_critical_logs import parse_report, TARGET_KEYS
from mysql_export import insert_records
from datetime import datetime

TABLE_NAME = "critical_logs"

FINAL_COLUMNS = TARGET_KEYS + [
    "REPORT_HOST",
    "REPORT_DATE",
    "REPORT_UUID"
]

def main():

    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"../../vm_system_reports/vm_system_report_{today}.log"

    records = parse_report(filename)

    print(f"Parsed {len(records)} structured log entries.")

    rows = [
        tuple(rec.get(col) for col in FINAL_COLUMNS)
        for rec in records
    ]

    insert_records(TABLE_NAME, FINAL_COLUMNS, rows)

if __name__ == "__main__":
    main()