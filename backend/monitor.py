# monitor.py

import asyncio
from playwright.async_api import async_playwright
import time

LAST_SEEN = None  # To store the last seen tweet


async def fetch_latest_tweet(username):
    global LAST_SEEN
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(f'https://twitter.com/{username}', timeout=60000)
            await page.wait_for_selector('article', timeout=10000)
            articles = await page.query_selector_all('article')

            latest_tweet = None
            for article in articles[:5]:  # Look through the first few tweets
                text = await article.inner_text()
                if "Pinned Tweet" in text and latest_tweet is None:
                    continue  # Skip pinned tweet if it's the first one
                elif "Pinned Tweet" not in text:
                    latest_tweet = text
                    break

            # Fallback: use pinned tweet if nothing else found
            if not latest_tweet and articles:
                latest_tweet = await articles[0].inner_text()

            return latest_tweet
        except Exception as e:
            print("Error fetching tweet:", e)
        finally:
            await browser.close()
    return None
