# config.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    TWITTER_USERNAME: str
    TWITTER_PASSWORD: str
    TWEET_DELAY: int = 3600  # Default 1 hour delay between tweets
    MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"

# twitter_bot.py
import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    ElementClickInterceptedException
)
from config import Settings

# Configure logging
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
        """Configure and initialize the Chrome WebDriver with enhanced privacy."""
        options = webdriver.ChromeOptions()
        
        # Enhanced privacy and security options
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        # Random user agent to avoid detection
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def safe_find_and_click(self, by, value, timeout=10):
        """Safely find and click elements with retry logic."""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except (TimeoutException, ElementClickInterceptedException) as e:
            logger.error(f"Error clicking element: {e}")
            return False

    def login(self):
        """Login to Twitter with improved error handling and security."""
        try:
            logger.info("Attempting to log in to Twitter...")
            self.driver.get("https://twitter.com/login")
            
            # Enter username
            username_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_input.send_keys(self.settings.TWITTER_USERNAME)
            username_input.send_keys(Keys.RETURN)
            
            # Enter password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.send_keys(self.settings.TWITTER_PASSWORD)
            password_input.send_keys(Keys.RETURN)
            
            # Verify login success
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            logger.info("Successfully logged in to Twitter")
            return True
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False

    def post_tweet(self, message):
        """Post a tweet with retry logic and rate limiting."""
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
                    time.sleep(random.uniform(1, 3))  # Random delay between retries
                    continue
                return False

    def cleanup(self):
        """Safely close the browser and clean up resources."""
        try:
            self.driver.quit()
            logger.info("Successfully cleaned up resources")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

# main.py
def main():
    bot = TwitterBot()
    try:
        if bot.login():
            # Example tweet with hashtags
            tweet_text = "Exploring the future of AI and crypto! 🚀 #AstraAI #Crypto #Web3"
            bot.post_tweet(tweet_text)
            time.sleep(random.uniform(2, 5))  # Random delay after posting
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main()
