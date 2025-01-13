import time
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables
load_dotenv()

# Retrieve credentials from environment variables
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

def login_and_tweet():
    # Launch Playwright and use Chromium in headless mode
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,  # Ensure headless mode is enabled
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']  # Additional arguments to avoid issues in containers
        )
        page = browser.new_page()

        # Navigate to Twitter login page
        page.goto("https://twitter.com/login")

        # Fill in the login details
        page.fill('input[name="text"]', TWITTER_USERNAME)
        page.fill('input[name="password"]', TWITTER_PASSWORD)
        page.click('div[data-testid="LoginForm_Login_Button"]')
        time.sleep(3)  # Adjust sleep to ensure the login is complete

        # Tweeting a message
        page.fill('div.DraftEditor-root', "Automated Tweet using Playwright!")
        page.click('div[data-testid="tweetButton"]')

        print("Tweet posted successfully!")

        # Close the browser after task is completed
        browser.close()

if __name__ == "__main__":
    login_and_tweet()
