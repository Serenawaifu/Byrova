from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import os

# Browser selector
BROWSER = os.getenv("BROWSER", "chrome").lower()  # Default is Chrome

def get_driver():
    if BROWSER == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    elif BROWSER == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=firefox_options)

    elif BROWSER == "edge":
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=edge_options)

    else:
        raise ValueError("Unsupported browser. Use 'chrome', 'firefox', or 'edge'.")

def login_to_twitter(driver):
    driver.get("https://twitter.com/login")
    time.sleep(2)

    # Find the login form fields and enter your credentials
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(os.getenv("TWITTER_USERNAME"))
    username_field.send_keys(Keys.RETURN)
    time.sleep(2)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(os.getenv("TWITTER_PASSWORD"))
    password_field.send_keys(Keys.RETURN)
    time.sleep(3)

def tweet_message(driver, message):
    driver.get("https://twitter.com/home")
    time.sleep(2)
    tweet_box = driver.find_element(By.CSS_SELECTOR, "div.DraftEditor-root")
    tweet_box.send_keys(message)
    tweet_button = driver.find_element(By.CSS_SELECTOR, "div[data-testid='tweetButton']")
    tweet_button.click()

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
