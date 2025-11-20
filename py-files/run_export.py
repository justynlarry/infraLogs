import os
from parse_critical_logs import parse_report, TARGET_KEYS
from mysql_export import insert_records
from datetime import datetime

TABLE_NAME = "critical_logs"

COLUMN_MAPPING = {
    'TIMESTAMP':        'record_time',
    'MESSAGE':           'message',
    '_HOSTNAME':        'hostname',
    '_COMM':            'command_name',
    '_PID':             'process_id',
    'PRIORITY':         'priority',
    'SYSLOG_IDENTIFIER':'syslog_id',
    'REPORT_HOST':      'report_host',
    'REPORT_DATE':      'report_date',
    'REPORT_UUID':      'report_uuid'
}

DB_COLUMNS = [
    "record_time",
    "message",
    "hostname",
    "command_name",
    "process_id",
    "priority",
    "syslog_id",
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