import re

def extract_host_metadata(block_lines):
    """ 
    Extracts metadata for a single host block:
        --- Host: NAME
        --- Date: YY-DD-MM
        --- UUID: XXXXXX
    """

    hostname = None
    date = None
    uuid = None
    for line in block_lines:
        line=line.strip()
        if not line:
            continue
        if line.startswith('--- Host:'):
            hostname = line.split(':', 1)[1].strip().split()[0]
        elif line.startswith('--- Date:'):
            date = line.split(':', 1)[1].strip().split()[0]
        elif line.startswith('--- UUID'):
            uuid = line.split(':', 1)[1].strip().split()[0]

    return hostname, date, uuid