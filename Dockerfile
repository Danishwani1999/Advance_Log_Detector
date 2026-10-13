FROM python:3.12-slim

WORKDIR /app

RUN useradd -u 1000 appuser && chown -R appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/metrics')"

CMD ["python", "main.py"]
