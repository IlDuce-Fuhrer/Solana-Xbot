# monitor_tweet.py
import asyncio
from playwright.async_api import async_playwright

username = "dulc1x"
last_tweet = None


async def fetch_latest_tweet(page, username):
    url = f"https://twitter.com/{username}"
    print(f"Navigating to {url}...")
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)

    try:
        # Wait for all tweets to appear
        await page.wait_for_selector("article", timeout=15000)
        tweet_articles = await page.query_selector_all("article")

        for article in tweet_articles:
            # Skip pinned tweet if it exists
            is_pinned = await article.query_selector('svg[aria-label="Pinned Tweet"]')
            if is_pinned:
                continue

            # Get only the visible tweet text from the current article
            text_nodes = await article.query_selector_all('div[lang]')
            tweet_lines = []
            for node in text_nodes:
                # Filter out quoted/replied tweet blocks (they appear inside nested sections)
                in_quote = await node.evaluate('(el) => el.closest("article") !== el.closest("div[lang]").closest("article")')
                if not in_quote:
                    tweet_lines.append(await node.inner_text())

            tweet_text = "\n".join(tweet_lines).strip()

            if tweet_text:
                return tweet_text  # Return the first valid, non-pinned tweet

        return None  # If nothing valid found

    except Exception as e:
        print("Error fetching tweet:", e)
        return None


async def monitor():
    global last_tweet
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="user_data",
            headless=False  # Set to True if you don’t want to see the browser
        )
        page = await browser.new_page()

        while True:
            tweet = await fetch_latest_tweet(page, username)
            if tweet and tweet != last_tweet:
                print("New tweet detected:")
                print(tweet)
                last_tweet = tweet
            else:
                print("No new tweet or tweet unchanged.")

            await asyncio.sleep(30)  # Check every 30 seconds

asyncio.run(monitor())
