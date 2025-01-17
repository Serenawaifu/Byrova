# Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.41.0

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Command to run the script
CMD ["python", "main.py"]

# docker-compose.yml
version: '3'
services:
  twitter-bot:
    build: .
    environment:
      - TWITTER_USERNAME=${TWITTER_USERNAME}
      - TWITTER_PASSWORD=${TWITTER_PASSWORD}
      - TWEET_DELAY=${TWEET_DELAY:-3600}
      - MAX_RETRIES=${MAX_RETRIES:-3}
    volumes:
      - .:/app
    restart: unless-stopped

# requirements.txt
playwright==1.41.0
python-dotenv==1.0.0

# main.py
import time
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError

# Load environment variables
load_dotenv()

# Retrieve credentials from environment variables
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
TWEET_DELAY = int(os.getenv('TWEET_DELAY', 3600))

def login_to_twitter(page):
    """Handle Twitter login with retry mechanism"""
    try:
        # Navigate to Twitter login page
        page.goto("https://twitter.com/i/flow/login", wait_until="networkidle")
        
        # Fill username and click next
        page.fill('input[autocomplete="username"]', TWITTER_USERNAME)
        page.click('div[role="button"]:has-text("Next")')
        
        # Wait for and fill password
        page.wait_for_selector('input[type="password"]')
        page.fill('input[type="password"]', TWITTER_PASSWORD)
        
        # Click login button
        page.click('div[role="button"]:has-text("Log in")')
        
        # Wait for home timeline to ensure we're logged in
        page.wait_for_selector('div[data-testid="primaryColumn"]', timeout=10000)
        return True
    except Exception as e:
        print(f"Login error: {str(e)}")
        return False

def post_tweet(page, message):
    """Post a tweet with error handling"""
    try:
        # Click tweet compose button
        page.click('a[href="/compose/tweet"]')
        
        # Wait for and fill tweet input
        page.wait_for_selector('div[data-testid="tweetTextarea_0"]')
        page.fill('div[data-testid="tweetTextarea_0"]', message)
        
        # Click tweet button
        page.click('div[data-testid="tweetButton"]')
        
        # Wait for tweet to be posted
        page.wait_for_selector('div[data-testid="toast"]', timeout=10000)
        return True
    except Exception as e:
        print(f"Tweet error: {str(e)}")
        return False

def main():
    """Main function with retry mechanism"""
    retry_count = 0
    
    while retry_count < MAX_RETRIES:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                
                context = browser.new_context(
                    viewport={'width': 1280, 'height': 800},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                page = context.new_page()
                
                if login_to_twitter(page):
                    tweet_message = f"Automated Tweet using Playwright! Posted at: {time.strftime('%Y-%m-%d %H:%M:%S')}"
                    if post_tweet(page, tweet_message):
                        print("Tweet posted successfully!")
                        break
                
                browser.close()
                
        except Exception as e:
            print(f"Attempt {retry_count + 1} failed: {str(e)}")
            retry_count += 1
            time.sleep(5)  # Wait before retrying
            
        if retry_count == MAX_RETRIES:
            print("Max retries reached. Exiting.")

if __name__ == "__main__":
    while True:
        main()
        print(f"Waiting {TWEET_DELAY} seconds before next tweet...")
        time.sleep(TWEET_DELAY)
