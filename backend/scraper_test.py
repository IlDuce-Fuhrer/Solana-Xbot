from playwright.async_api import async_playwright
import asyncio


async def fetch_latest_tweet(username):
    url = f"https://twitter.com/{username}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print(f"Navigating to {url}...")
            await page.goto(url, wait_until="domcontentloaded", timeout=20000)
            await page.wait_for_selector("article", timeout=10000)

            tweets = await page.locator("article").all()
            if not tweets:
                print("No tweets found.")
                return None

            tweet_texts = [await t.inner_text() async for t in tweets[:2]]
            tweet = tweet_texts[1] if "Pinned Tweet" in tweet_texts[0] else tweet_texts[0]
            return tweet.strip()

        except Exception as e:
            print(f"Error fetching tweet: {e}")
            return None
        finally:
            await browser.close()

# Example usage
# asyncio.run(fetch_latest_tweet("dulc1x"))
