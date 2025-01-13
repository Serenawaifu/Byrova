from playwright.sync_api import sync_playwright
import os
import time

def login_to_twitter(page):
    page.goto("https://twitter.com/login")
    time.sleep(2)

    # Fill in username and password
    page.fill("input[name='text']", os.getenv("TWITTER_USERNAME"))
    page.keyboard.press("Enter")
    time.sleep(2)

    page.fill("input[name='password']", os.getenv("TWITTER_PASSWORD"))
    page.keyboard.press("Enter")
    time.sleep(3)

def tweet_message(page, message):
    page.goto("https://twitter.com/home")
    time.sleep(2)
    page.locator("div[aria-label='Tweet text']").fill(message)
    page.locator("div[data-testid='tweetButton']").click()

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            login_to_twitter(page)
            tweet_message(page, "Automated tweet using Playwright! #AstraAI #Crypto")
            time.sleep(5)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
