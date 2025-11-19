import re
from parse_metadata import extract_host_metadata
from datetime import datetime, date

# DEFINE TARGET KEYS:
TARGET_KEYS = [
    'TIMESTAMP',        # Special key from the date line (datetime object)
    'MESSAGE',          # The actual log message content
    '_HOSTNAME',
    '_COMM',            # The command name (e.g., kubelet)
    '_PID',
    'PRIORITY',
    'SYSLOG_IDENTIFIER'
]
RECROD_START_RE = re.compile(
    r'^\w{3}\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{6}\s\w{3}(\s+\[.*\]| \[.*\])$'
)

def parse_report(filename):
    """
    Input:  A full Ansible Report containing multiple hosts.
    Output: A list of parsed log dicitionaries.
    """

    with open(filename, "r") as f:
        lines = f.readlines()

    blocks = []
    current = []

    for line in lines:
        if line.startswith('--- Host:') and current:
            blocks.append(current)
            current = []
        current.append(line)

    if current:
        blocks.append(current)
    
    all_records = []

    for block in blocks:
        hostname, report_date, uuid = extract_host_metadata(block)

        try:
            start_idx = next(
                i for i, l in enumerate(block)
                if l.startswith('--- CRITICAL LOGS BY PRIORITY ---')
            )
        except StopIteration:
            continue

        record_lines = block[start_idx +1:]

        current_record = {}
        for i, lin in enumerate(record_lines):
            line = line.rstrip()

            if RECORD_START_RE.match(line):

                if current_record:
                    current_record["REPORT_HOST"] = hostname
                    current_record["REPORT_DATE"] = report_date
                    current_record["REPORT_UUID"] = uuid
                    all_records.append(current_record)
                current_record = {}

                timestamp_part = line.split(" [")[0]
                try:
                    dt = datetime.strptime(
                        timestamp_part, "%a %Y-%m-%d %H:%M:%S.%f %Z"
                     )
                    current_record["TIMESTAMP"] = dt
                except:
                    current_record["TIMESTAMP"] = timestamp_part
            elif current_record and "=" in line:
                k, v = line.strip().split("=", 1)
                k = k.strip()
                v = v.strip()

                if k.upper() in TARGET_KEYS:
                    current_record[k.upper()] = v
        
        if current_record:
            current_record["REPORT_HOST"] = hostname
            current_record["REPORT_DATE"] = report_date
            current_record["REPORT_UUID"] = uuid
            all_records.append(current_record)
    return all_records
