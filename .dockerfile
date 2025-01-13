# Use Python 3.11-slim as the base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y wget curl gnupg libnss3 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 libxkbcommon0 \
    libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0 \
    libdrm2 libasound2 unzip && apt-get clean

# Install Playwright and Python dependencies
RUN pip install --no-cache-dir playwright==1.40.0 python-dotenv
RUN playwright install --with-deps

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Expose shared memory for stability
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN mkdir /tmp/browser && chmod -R 1777 /tmp/browser

# Run the bot
CMD ["python", "twitter_bot.py"]
