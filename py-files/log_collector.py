import subprocess
import re
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

def parse_journalctl_verbose_today_filtered():
    """
    Executes 'journalctl --since today', parses the output, 
    and returns a list of dictionaries (records) containing ONLY the TARGET_KEYS.
    """
    
    journalctl_command = ["journalctl", "-o", "verbose", "--no-pager", "--since", "today"]

    print(f"Executing command: {' '.join(journalctl_command)}")

    try:
        result = subprocess.run(
            journalctl_command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        log_output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running journalctl: {e}")
        print(f"Stderr: {e.stderr}")
        return []

    # Initialize storage
    records = []
    current_record = {}
    
    timestamp_pattern = re.compile(r'^\w{3}\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{6}\s\w{3}(\s+\[.*\]| \[.*\])$')
    lines = log_output.splitlines()

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # 1. Start of a new record
        if timestamp_pattern.match(line):
            # If the current record is complete, filter and store it
            if current_record:
                # --- NEW FILTERING LOGIC ---
                filtered_record = {
                    key: current_record.get(key)
                    for key in TARGET_KEYS 
                    if key in current_record # Only include keys that were found in the log
                }
                records.append(filtered_record)
                # ---------------------------

            current_record = {}
            
            # Parsing the date/time (always done to set the 'TIMESTAMP' field)
            date_match = re.search(r'^(\w{3}\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{6}\s\w{3})', line)
            if date_match:
                full_date_string = date_match.group(1)
                try:
                    dt_obj = datetime.strptime(full_date_string, '%a %Y-%m-%d %H:%M:%S.%f %Z')
                    current_record['TIMESTAMP'] = dt_obj
                except ValueError:
                    # Storing string as fallback, but only if 'TIMESTAMP' is a target key
                    if 'TIMESTAMP' in TARGET_KEYS:
                        current_record['TIMESTAMP_STRING'] = full_date_string
            
            # Parsing the structured metadata (s, i, b, m, t, x)
            metadata_match = re.search(r'\[(.*)\]', line)
            if metadata_match:
                metadata_str = metadata_match.group(1)
                for item in metadata_str.split(';'):
                    if '=' in item:
                        key, value = item.split('=', 1)
                        # We only temporarily store these keys if they are in the TARGET_KEYS
                        if key.upper() in TARGET_KEYS:
                            current_record[key.upper()] = value
            
        # 2. Handle regular key-value lines
        elif current_record and '=' in line:
            key, value = line.split('=', 1)
            # --- MODIFIED CAPTURE LOGIC ---
            # Only store the key if it's in the list of target keys
            if key.upper().strip() in TARGET_KEYS:
                current_record[key.upper().strip()] = value.strip()
            # ------------------------------

    # Append the very last record
    if current_record:
        # --- NEW FILTERING LOGIC ---
        filtered_record = {
            key: current_record.get(key)
            for key in TARGET_KEYS 
            if key in current_record
        }
        records.append(filtered_record)
        
    return records

# --- Execution Example ---
parsed_records_filtered = parse_journalctl_verbose_today_filtered()

print(f"\nSuccessfully parsed {len(parsed_records_filtered)} log records.")
if parsed_records_filtered:
    print(f"\n--- First Filtered Record (Keys Used: {', '.join(TARGET_KEYS)}) ---")
    for key, value in parsed_records_filtered[0].items():
        print(f"**{key}**: {value}")
