FROM python:3.11-slim

WORKDIR /app

# Install netcat
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set execute permissions explicitly
RUN chmod +x /app/entrypoint.sh && \
    chmod +x /app/manage.py

EXPOSE 8000

# Use shell form to ensure proper script execution
CMD ["/bin/bash", "/app/entrypoint.sh"] 