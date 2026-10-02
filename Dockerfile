FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . .

# Expose port for Prometheus metric scraping
EXPOSE 8000

# Start the metrics exporter service
CMD ["python", "exporter.py"]
