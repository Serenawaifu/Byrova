from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Set up ChromeDriver with WebDriver Manager
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN", "/usr/bin/google-chrome")

    # Use WebDriver Manager to install and set up ChromeDriver
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Login to Twitter
def login_to_twitter(driver):
    driver.get("https://twitter.com/login")
    time.sleep(2)

    username = driver.find_element(By.NAME, "text")
    username.send_keys(os.getenv("TWITTER_USERNAME"))
    username.send_keys(Keys.RETURN)
    time.sleep(2)

    password = driver.find_element(By.NAME, "password")
    password.send_keys(os.getenv("TWITTER_PASSWORD"))
    password.send_keys(Keys.RETURN)
    time.sleep(3)

# Post a tweet
def tweet_message(driver, message):
    driver.get("https://twitter.com/home")
    time.sleep(2)
    tweet_box = driver.find_element(By.CSS_SELECTOR, "div.DraftEditor-root")
    tweet_box.send_keys(message)
    tweet_button = driver.find_element(By.CSS_SELECTOR, "div[data-testid='tweetButton']")
    tweet_button.click()

# Main function
def main():
    driver = get_driver()
    try:
        login_to_twitter(driver)
        tweet_message(driver, "Automated tweet using Selenium! #AstraAI #Crypto")
        time.sleep(5)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
