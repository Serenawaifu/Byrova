import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    TWITTER_USERNAME: str
    TWITTER_PASSWORD: str
    TWEET_DELAY: int = 3600
    MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TwitterBot:
    def __init__(self):
        self.settings = Settings()
        self.setup_driver()

    def setup_driver(self):
        """Configure and initialize the Chrome WebDriver for Railway"""
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-notifications')
            options.binary_location = "/usr/bin/chromium"
            
            service = Service(executable_path="/usr/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=options)
            
            self.wait = WebDriverWait(self.driver, 15)  # Increased wait time
            logger.info("Successfully initialized Chrome browser")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    def check_login_status(self):
        """Check if already logged in"""
        try:
            self.driver.get("https://twitter.com/home")
            time.sleep(5)  # Wait for any redirects
            tweet_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            logger.info("Already logged in to Twitter")
            return True
        except:
            logger.info("Not logged in, proceeding with login")
            return False

    def login(self):
        """Login to Twitter with improved error handling"""
        try:
            if self.check_login_status():
                return True

            logger.info("Attempting to log in to Twitter...")
            self.driver.get("https://twitter.com/i/flow/login")
            time.sleep(5)  # Wait for page load
            
            # Enter username
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_input.clear()
            username_input.send_keys(self.settings.TWITTER_USERNAME)
            username_input.send_keys(Keys.RETURN)
            time.sleep(2)
            
            # Enter password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(self.settings.TWITTER_PASSWORD)
            password_input.send_keys(Keys.RETURN)
            
            # Wait for login completion
            time.sleep(5)
            
            # Verify login
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            logger.info("Successfully logged in to Twitter")
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False

    def post_tweet(self, message):
        """Post a tweet with improved error handling"""
        for attempt in range(self.settings.MAX_RETRIES):
            try:
                # Make sure we're on the home page
                self.driver.get("https://twitter.com/home")
                time.sleep(3)
                
                # Find and click tweet button
                tweet_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
                )
                tweet_button.click()
                time.sleep(1)
                
                # Find tweet input and enter message
                tweet_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
                )
                tweet_input.clear()
                tweet_input.send_keys(message)
                time.sleep(1)
                
                # Click post button
                post_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
                )
                post_button.click()
                time.sleep(3)
                
                logger.info(f"Successfully posted tweet: {message[:50]}...")
                return True
                
            except Exception as e:
                logger.error(f"Error posting tweet (attempt {attempt + 1}/{self.settings.MAX_RETRIES}): {e}")
                if attempt < self.settings.MAX_RETRIES - 1:
                    time.sleep(random.uniform(2, 5))
                    continue
                return False

    def cleanup(self):
        """Clean up resources"""
        try:
            if hasattr(self, 'driver'):
                self.driver.quit()
            logger.info("Successfully cleaned up resources")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main():
    bot = TwitterBot()
    try:
        if bot.login():
            tweet_text = "Exploring the future of AI and crypto! 🚀 #AstraAI #Crypto #Web3"
            bot.post_tweet(tweet_text)
            time.sleep(random.uniform(2, 5))
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main()
