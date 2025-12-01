import re
from parse_metadata import extract_host_metadata
from datetime import datetime

# Define Target Keys:
TARGET_KEYS = [
    'UNIT',
    'LOAD',
    'ACTIVE',
    'SUB',
    'DESCRIPTION'
]

def parse_failed_svc(filename):
    """
    Parse Failed Services information from the vm_system_report
    Returns a list of dictionaries with storage data
    """

    with open(filename, "r") as f:
        lines = f.readlines()
    # Split into blocks by host
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
                if l.startswith('===BEGIN:FAILED_SERVICES===')
            )
            end_idx = next(
                i for i, l in enumerate(block)
                if l.startswith('===END:FAILED_SERVICES===')
            )
        except StopIteration:
            continue
        storage_lines = block[start_idx + 1:end_idx]

        for line in storage_lines:
            line=line.rstrip()

            if not line or line.startswith('  UNIT'):
                continue

            if not line or line.startswith("0 loaded units listed."):
                continue

            fields = line.split()
            if len(fields) >=5:
                record = {
                    "UNIT":         fields[0],
                    "LOAD":         fields[1],
                    "ACTIVE":       fields[2],
                    "SUB":          fields[3],
                    "DESCRIPTION":  fields[4],
                    "REPORT_HOST":      hostname,
                    "REPORT_DATE":      report_date,
                    "REPORT_UUID":      uuid
                }
                all_records.append(record)
    return all_records