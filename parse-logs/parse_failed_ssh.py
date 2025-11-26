import re
from parse_metadata import extract_host_metadata
from datetime import datetime

TARGET_KEYS = [
    'TIMESTAMP',
    'SOURCE_IP',
    'SOURCE_PORT',
    'ATTEMPTED_USER',
    'LOG_LINE',
    'FAILURE_TYPE',
    'INVALID_USER'
]

SSH_FAILURE_PATTERNS = [
    r'Failed password for (?:invalid user )?(\S+) from ([\d.]+) port (\d+)',
    r'Invalid user (\S+) from ([\d.]+) port (\d+)',
    r'Connection closed by (?:invalid user |authenticating user )?(\S+) ([\d.]+) port (\d+)',
]

def parse_failed_ssh(filename):
    """
    Parse Failed SSH Login attempts from the vm_system_report
    Returns a list of dictionaries with SSH Failure data
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
                if l.startswith('===BEGIN:FAILED_SSH===')
            )
            end_idx = next(
                i for i, l in enumerate(block)
                if l.startswith('===END:FAILED_SSH===')
            )
        except StopIteration:
            continue
        
        ssh_lines = block[start_idx + 1:end_idx]
        
        for line in ssh_lines:
            line = line.rstrip()
            
            if not line:
                continue
            
            # Extract timestamp
            timestamp_match = re.match(r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', line)
            if timestamp_match:
                ts_str = timestamp_match.group(1)
                # Extract year from report_date (format: "YYYY-MM-DD")
                year = report_date.split('-')[0]
                # Parse the timestamp with the year
                try:
                    timestamp = datetime.strptime(f"{year} {ts_str}", "%Y %b %d %H:%M:%S")
                except ValueError:
                    timestamp = None
            else:
                timestamp = None
            
            for pattern in SSH_FAILURE_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    record = {
                        "REPORT_HOST":         hostname,
                        "REPORT_DATE":      report_date,
                        "REPORT_UUID":             uuid,
                        "TIMESTAMP":        timestamp,
                        "SOURCE_IP":        match.group(2) if len(match.groups()) >= 2 else None,
                        "SOURCE_PORT":      match.group(3) if len(match.groups()) >= 3 else None,
                        "ATTEMPTED_USER":   match.group(1),
                        "LOG_LINE":         line,
                        "FAILURE_TYPE":     None,
                        "INVALID_USER":     False
                    }
                    
                    # Determine failure type
                    if "Failed password" in line:
                        record["FAILURE_TYPE"] = "failed_password"
                        record["INVALID_USER"] = "invalid user" in line
                    elif "Invalid user" in line:
                        record["FAILURE_TYPE"] = "invalid_user"
                        record["INVALID_USER"] = True
                    elif "Connection closed" in line:
                        record["FAILURE_TYPE"] = "connection_closed"
                        record["INVALID_USER"] = "invalid user" in line
                    
                    all_records.append(record)
                    break  # Stop after first matching pattern
    
    return all_records