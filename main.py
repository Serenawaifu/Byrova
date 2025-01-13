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
from selenium.common.exceptions import TimeoutException
from pydantic_settings import BaseSettings

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
            
            # For Railway's environment
            self.driver = webdriver.Chrome(options=options)
            
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("Successfully initialized Chrome browser")
            
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    def login(self):
        """Login to Twitter"""
        try:
            logger.info("Attempting to log in to Twitter...")
            self.driver.get("https://twitter.com/login")
            
            # Wait for and find username field
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_input.send_keys(self.settings.TWITTER_USERNAME)
            username_input.send_keys(Keys.RETURN)
            
            # Wait for and find password field
            password_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.send_keys(self.settings.TWITTER_PASSWORD)
            password_input.send_keys(Keys.RETURN)
            
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
        """Post a tweet"""
        for attempt in range(self.settings.MAX_RETRIES):
            try:
                # Find and click tweet button
                tweet_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
                )
                tweet_button.click()
                
                # Find tweet input and enter message
                tweet_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
                )
                tweet_input.send_keys(message)
                
                # Click post button
                post_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
                )
                post_button.click()
                
                logger.info(f"Successfully posted tweet: {message[:50]}...")
                return True
                
            except Exception as e:
                logger.error(f"Error posting tweet (attempt {attempt + 1}/{self.settings.MAX_RETRIES}): {e}")
                if attempt < self.settings.MAX_RETRIES - 1:
                    time.sleep(random.uniform(1, 3))
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
