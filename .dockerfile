# Use Python 3.11-slim as the base image
FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y wget curl gnupg libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 libxkbcommon0 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0 libdrm2 libasound2 unzip && apt-get clean

# Install Playwright and Python dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && playwright install --with-deps

# Copy the bot files into the container
COPY . .

# Command to run the bot
CMD ["python", "main.py"]
