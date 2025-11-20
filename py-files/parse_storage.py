import re
import pandas as pd
from parse_metadata import extract_host_metadata
from datetime import datetime

# DEFINE TARGET KEYS:
TARGET_KEYS = [
    'FILE_SYSTEM',
    'SIZE',
    'USED',
    'AVAIL',
    'USE_PERCENTAGE',
    'MOUNTED_ON'
]

def RECORD_START_RE(lines, hostname, date, uuid):
    data = []
    for line in lines:
        fields = line.split()
        if len(fields) >=6 and not line.startswith("Filesystem"):
            data.append({
                "Filesystem":   fields[0],
                "Size":         fields[1],
                "Used":         fields[2],
                "Avail":        fields[3],
                "Use%":         fields[4],
                "Mounted On":   fields[5]
            })
    return pd.DataFrame(data)

def parse_storage(filename):
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
                if l.startswith('===BEGIN:STORAGE===')
            )
        except StopIteration:
            continue

        record_lines = block[start_idx +1:]

        current_record = {}
        for i, line in enumerate(record_lines):
            line=line.rstrip()

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
                k, v = line.strip().split("=",1)
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
