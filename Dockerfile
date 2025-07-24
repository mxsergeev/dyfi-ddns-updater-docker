FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY dyfi_ddns_updater.py .

# Define volume for state/log persistence
VOLUME ["/data"]

# Default command: pulls config from environment
CMD ["python", "-u", "dyfi_ddns_updater.py"]