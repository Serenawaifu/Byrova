from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

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

    # Find the login form fields and enter your credentials
    username = driver.find_element("name", "text")
    password = driver.find_element("name", "password")

    username.send_keys("NyrovaAI")
    password.send_keys("DFtB@5475")

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

if __name__ == "__main__":
    main()