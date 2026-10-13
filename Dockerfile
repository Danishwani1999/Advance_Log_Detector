FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source and set ownership
COPY detector.py .
COPY sample_system.log .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "-u", "detector.py"]

