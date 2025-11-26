import os
from datetime import datetime

# Define the correct path
today = datetime.today().strftime("%Y-%m-%d")
filename = f"../../vm_system_reports/vm_system_report_{today}.log"

print(f"Checking for file: {filename}")

# Check if the file exists and is readable
if os.path.exists(filename):
    print("SUCCESS: File exists.")
    try:
        # Attempt to read the file contents
        with open(filename, 'r') as f:
            content = f.read()
            # Check the size of the content
            print(f"SUCCESS: Read {len(content)} characters.")
            
            # Print the first 500 characters to confirm content (optional)
            # print("--- Start of Log ---")
            # print(content[:500])
            # print("--- End of Log ---")
            
    except Exception as e:
        # Catch any permission or I/O errors
        print(f"ERROR: Failed to read file: {e}")
else:
    print("ERROR: File does NOT exist at the calculated path.")