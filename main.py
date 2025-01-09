from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import os  # Import the os module for environment variables

# Set up Chrome options to run headlessly
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Path to ChromeDriver (will be handled by Railway)
driver = webdriver.Chrome(options=options)

def login_to_twitter():
    driver.get("https://twitter.com/login")
    time.sleep(2)

    # Get credentials from environment variables
    twitter_username = os.getenv("TWITTER_USERNAME")
    twitter_password = os.getenv("TWITTER_PASSWORD")

    if not twitter_username or not twitter_password:
        print("Error: Missing Twitter credentials in environment variables.")
        driver.quit()
        return

    # Find the login form fields and enter your credentials
    username = driver.find_element("name", "text")
    username.send_keys(twitter_username)
    username.send_keys(Keys.RETURN)
    time.sleep(2)

    password = driver.find_element("name", "password")
    password.send_keys(twitter_password)
    password.send_keys(Keys.RETURN)
    time.sleep(3)

def tweet_message(message):
    tweet_box = driver.find_element("css selector", "div.DraftEditor-root")
    tweet_box.send_keys(message)
    tweet_button = driver.find_element("css selector", "div[data-testid='tweetButton']")
    tweet_button.click()

def main():
    login_to_twitter()
    tweet_message("Automated tweet using Selenium! #AstraAI #Crypto")
    time.sleep(5)
    driver.quit()  # Close the browser after execution

if __name__ == "__main__":
    main()
