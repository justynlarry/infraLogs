import re
from parse_failed_ssh import parse_failed_ssh, TARGET_KEYS
from mysql_export import insert_records
from parse_metadata import extract_host_metadata
from datetime import datetime

TABLE_NAME = "failed_ssh"

COLUMN_MAPPING = {
    'TIMESTAMP':        'timestamp',
    'SOURCE_IP':        'source_ip',
    'SOURCE_PORT':      'source_port',
    'ATTEMPTED_USER':   'attempted_user',
    'LOG_LINE':         'log_line',
    'REPORT_HOST':      'report_host',
    'REPORT_DATE':      'report_date',
    'REPORT_UUID':      'report_uuid'
}

DB_COLUMMS = [
    "timestamp",
    "source_ip",
    "source_port",
    "attempted_user",
    "log_line",
    "report_host",
    "report_date",
    "report_uuid"
]

def main():
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"../../vm_system_reports/vm_system_report_{today}.log"

    records = parse_report(filename)

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