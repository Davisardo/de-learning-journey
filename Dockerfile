# Base image — Python 3.13
FROM python:3.13-slim

# Set working directory di dalam container
WORKDIR /app

# Copy requirements dulu (untuk cache)
COPY requirements.txt .

# Install semua library
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua kode
COPY . .

# Jalankan ETL pipeline saat container start
CMD ["python", "etl_final.py"]