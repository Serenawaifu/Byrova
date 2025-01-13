# Use Python 3.12 slim base image
FROM python:3.12-slim

# Install system dependencies required for Playwright and headless browser support
RUN apt-get update && apt-get install -y wget curl gnupg2 libgbm-dev

# Install dependencies from requirements.txt and Playwright
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps

# Set working directory inside the container
WORKDIR /app

# Copy your entire project code into the container
COPY . .

# Expose port for debugging or health checks (if needed)
EXPOSE 9222

# Command to run your Python script (main.py)
CMD ["python", "main.py"]
