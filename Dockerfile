# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make CLI executable
RUN chmod +x cli.py test_router.py app.py

# Expose port for Flask app
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command runs the Flask app
CMD ["python", "app.py"]
