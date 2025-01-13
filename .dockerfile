# Use Python 3.8-slim base image
FROM python:3.8-slim

# Install dependencies for Selenium and Web Browsers
RUN apt-get update && apt-get install -y wget gnupg2 curl unzip \
    libnss3 libgconf-2-4 libfontconfig1 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libatk-bridge2.0-0 \
    libcups2 libxrandr2 libasound2 libpangocairo-1.0-0 libgtk-3-0 libgbm-dev \
    firefox-esr \
    && apt-get clean

# Install Python dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY . .

# Start the bot
CMD ["python", "main.py"]
