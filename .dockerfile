# Use Python 3.8-slim as base image
FROM python:3.8-slim

# Install required dependencies for Selenium and Chrome
RUN apt-get update && apt-get install -y wget gnupg2 curl unzip \
    libnss3 libgconf-2-4 libfontconfig1 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libatk-bridge2.0-0 \
    libcups2 libxrandr2 libasound2 libpangocairo-1.0-0 libgtk-3-0 libgbm-dev \
    && apt-get clean

# Install Chrome browser
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install

# Set up environment variable for Chrome binary path
ENV GOOGLE_CHROME_BIN=/usr/bin/google-chrome

# Install Python dependencies
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY . .

# Install webdriver-manager
RUN pip install webdriver-manager

# Default command to run the bot
CMD ["python", "twitter_bot.py"]
