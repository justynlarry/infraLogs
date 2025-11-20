import re
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

def parse_storage(filename):
    """
    Parse storage information from the vm_system_report
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
                if l.startswith('===BEGIN:STORAGE===')
            )
            end_idx = next(
                i for i, l in enumerate(block)
                if l.startswith('===END:STORAGE===')
            )
        except StopIteration:
            continue

        storage_lines = block[start_idx + 1:end_idx]

        
        for line in storage_lines:
            line=line.rstrip()

            if not line or line.startwith('Filesystem'):
                continue

            fields = line.split()
            if len(fields) >=6:
                record = {
                "Filesystem":   fields[0],
                "Size":         fields[1],
                "Used":         fields[2],
                "Avail":        fields[3],
                "Use%":         fields[4],
                "Mounted On":   fields[5],
                "REPORT_HOST":  hostname,
                "REPORT_DATE":  report_date,
                "REPORT_UUID":  uuid
                }
                all_records.append(record)
    return all_records
