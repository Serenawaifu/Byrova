from playwright.sync_api import sync_playwright
import time
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve credentials from environment variables
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

def login_and_tweet():
    # Launch Playwright and use Chromium in headless mode
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run headless (no GUI)
        page = browser.new_page()
        
        # Navigate to Twitter login page
        page.goto("https://twitter.com/login")
        
        # Wait for the login fields to load and perform login
        page.fill('input[name="text"]', TWITTER_USERNAME)
        page.fill('input[name="password"]', TWITTER_PASSWORD)
        page.click('div[data-testid="LoginForm_Login_Button"]')
        time.sleep(3)  # Adjust the sleep time as needed to ensure the login is complete
        
        # Tweeting a message
        page.fill('div.DraftEditor-root', "Automated Tweet using Playwright!")
        page.click('div[data-testid="tweetButton"]')

        print("Tweet posted successfully!")

        # Close the browser after the task is done
        browser.close()

if __name__ == "__main__":
    login_and_tweet()
