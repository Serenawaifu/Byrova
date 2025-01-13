# Use Python 3.12 slim base image
FROM python:3.12-slim

# Install system dependencies for Playwright and headless browser support
RUN apt-get update && apt-get install -y wget curl gnupg2 libgbm-dev

# Install Playwright dependencies and browsers
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project code into the container
COPY . .

# Set the command to run your bot script
CMD ["python", "main.py"]
