
# Use Python Runtime as Base Image
FROM python:3.11-slim

# Set Working Directory
WORKDIR /log-display

# Install system dependencies
RUN apt update && apt-get install -y \
	gcc \
	&& rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /log-display
USER appuser

# Expose Port
EXPOSE 5000

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run Application
CMD ["python", "storage_display.py"]
