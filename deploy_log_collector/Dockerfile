# Python Slim Image
FROM python:3.12-slim-bookworm

# Working directory in container
WORKDIR /app

# Requirements and Dependencies
COPY requirements.txt .
COPY entrypoint.sh /app/

# Create and Activate Virtual Environment
RUN python3 -m venv opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && /opt/venv/bin/pip install pymysql python-dotenv 
RUN chmod +x /app/entrypoint.sh

# Add venv to Path
ENV PATH="/opt/venv/bin:$PATH"

# Copy Application Code
COPY . .

# Application Run Command
CMD ["python3", "mysql_export.py"]
CMD ["./entrypoint.sh"]
