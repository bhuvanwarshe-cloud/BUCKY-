# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
# PYTHONUNBUFFERED=1 prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
# PYTHONDONTWRITEBYTECODE=1 prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
# gcc and python3-dev might be needed for some packages
# ffmpeg is often required for audio processing
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the proper command for production
# "start" is standard for livekit agents in production
CMD ["python", "agent2.py", "start"]
