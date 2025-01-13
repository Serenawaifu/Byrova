import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import time

# Load environment variables
load_dotenv()

TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

# Ensure credentials are loaded
if not TWITTER_USERNAME or not TWITTER_PASSWORD:
    raise ValueError("Twitter credentials are missing from the .env file!")

def login_to_twitter(page):
    # Navigate to Twitter login page
    page.goto("https://twitter.com/login")
    time.sleep(2)

    # Find and fill in the username and password fields
    page.fill("input[name='text']", TWITTER_USERNAME)
    page.fill("input[name='password']", TWITTER_PASSWORD)
    
    # Submit the form
    page.click("div[data-testid='LoginForm_Login_Button']")
    time.sleep(3)

def tweet_message(page, message):
    # Find the tweet box and type the message
    page.fill("div[aria-label='Tweet text']", message)
    
    # Click the tweet button
    page.click("div[data-testid='tweetButton']")
    time.sleep(2)

def main():
    with sync_playwright() as p:
        # Launch the browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            login_to_twitter(page)
            tweet_message(page, "Automated tweet using Playwright! #AstraAI #Crypto")
        finally:
            # Close the browser after operation
            browser.close()

if __name__ == "__main__":
    main()
