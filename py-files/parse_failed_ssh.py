import re
from parse_metadata import extract_host_metadata
from datetime import datetime

TARGET_KEYS = [
    'TIMESTAMP',
    'SOURCE_IP',
    'SOURCE_PORT',
    'ATTEMPTED_USER',
    'LOG_LINE'
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
                for pattern in SSH_FAILURE_PATTERNS:
                    match = re.search(pattern, line)
                    if match:
                        record = {
                            "hostname":         "hostname",
                            "report_date":      "report_date",
                            "uuid":             "uuid",
                            "timestamp":        "timestamp",
                            "source_ip":        match.group(2) if len(match.groups()) >= 2 else None,
                            "source_port":      match.group(3) if len(match.groups()) >=3 else None,
                            "attempted_user":   match.group(1),
                            "log_line":         line
                        }

                        if "Failed password" in line:
                            record["failure_type"] = "failed_password"
                            record["invalid_user"] = "invalid user" in line
                    elif "Invalid user" in line:
                        record["failure_type"] = "invalid_user"
                        record["invalid_user"] = True
                    elif "Connection closed" in line:
                        record["failure_type"] = "connection_closed"
                        record["invalid_user"] = "invalid user" in line
                    
                    all_records.append(record)
                    break
    return all_records