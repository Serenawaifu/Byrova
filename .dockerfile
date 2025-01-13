# Use Python 3.8-slim base image
FROM python:3.8-slim

# Install dependencies for Selenium, Chrome, and ChromeDriver
RUN apt-get update && apt-get install -y wget gnupg2 curl unzip \
    libnss3 libgconf-2-4 libfontconfig1 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libatk-bridge2.0-0 \
    libcups2 libxrandr2 libasound2 libpangocairo-1.0-0 libgtk-3-0 libgbm-dev \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -y -f install \
    && wget -q "https://chromedriver.storage.googleapis.com/131.0.6778.265/chromedriver_linux64.zip"
