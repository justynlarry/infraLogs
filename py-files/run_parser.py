import sys
import subprocess

scripts = [
    "critical_logs_export.py",
    "storage_export.py"
]

for script in scripts:
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)

    print(f"Ran {script}")
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
