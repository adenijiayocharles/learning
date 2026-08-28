FROM python:3.12-slim

WORKDIR /app

# Dependencies change less often than application source, so install them first.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
