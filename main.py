import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

if not TWITTER_USERNAME or not TWITTER_PASSWORD:
    raise ValueError("Twitter username or password not found in environment variables.")

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Set ChromeDriver service
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

def login_to_twitter():
    driver.get("https://twitter.com/login")
    time.sleep(3)

    # Enter username
    username_input = driver.find_element("name", "text")
    username_input.send_keys(TWITTER_USERNAME)
    username_input.send_keys(Keys.RETURN)
    time.sleep(2)

    # Enter password
    password_input = driver.find_element("name", "password")
    password_input.send_keys(TWITTER_PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

def tweet_message(message):
    driver.get("https://twitter.com/compose/tweet")
    time.sleep(3)

    # Find the tweet box and post a message
    tweet_box = driver.find_element("css selector", "div.DraftEditor-root")
    tweet_box.click()
    tweet_box.send_keys(message)

    # Click the Tweet button
    tweet_button = driver.find_element("css selector", "div[data-testid='tweetButton']")
    tweet_button.click()
    time.sleep(3)

def main():
    try:
        login_to_twitter()
        tweet_message("Automated tweet using Selenium! #Crypto #Automation")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
