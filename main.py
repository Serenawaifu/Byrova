from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from pydantic_settings import BaseSettings

# Load environment variables using pydantic-settings
class Settings(BaseSettings):
    twitter_username: str
    twitter_password: str

    class Config:
        env_file = ".env"

# Load the settings
settings = Settings()

# Set up Chrome options to run headlessly
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)

# Login function
def login_to_twitter():
    driver.get("https://twitter.com/login")
    time.sleep(2)

    # Find the login fields and fill them with credentials
    username = driver.find_element("name", "text")
    username.send_keys(settings.twitter_username)
    username.send_keys(Keys.RETURN)
    time.sleep(2)

    password = driver.find_element("name", "password")
    password.send_keys(settings.twitter_password)
    password.send_keys(Keys.RETURN)
    time.sleep(3)

# Tweeting function
def tweet_message(message):
    time.sleep(5)  # Ensure page is fully loaded
    tweet_box = driver.find_element("css selector", "div.DraftEditor-root")
    tweet_box.click()
    tweet_box.send_keys(message)
    time.sleep(1)
    tweet_button = driver.find_element("css selector", "div[data-testid='tweetButton']")
    tweet_button.click()

# Main function to orchestrate the process
def main():
    try:
        login_to_twitter()
        tweet_message("Automated tweet using Selenium! #AstraAI #Crypto")
        time.sleep(5)
    finally:
        driver.quit()  # Close the browser

if __name__ == "__main__":
    main()
