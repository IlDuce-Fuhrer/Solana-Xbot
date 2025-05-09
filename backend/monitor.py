from playwright.sync_api import sync_playwright

def fetch_latest_tweet(username):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./user_data",  # Persistent session
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        try:
            print(f"Opening Twitter profile for @{username}...")
            page.goto(f"https://twitter.com/{username}", timeout=60000)
            page.wait_for_selector("article", timeout=15000)
            articles = page.query_selector_all("article")

            for i, article in enumerate(articles):
                html = article.inner_html()

                if "Pinned Tweet" in html:
                    continue  # Skip pinned tweet

                # Skip quote tweets
                if 'aria-label="Timeline: Conversation"' in html or "Quoted Tweet" in html:
                    continue

                tweet_parts = article.query_selector_all("div[lang]")
                tweet = "\n".join(part.inner_text().strip() for part in tweet_parts)

                if tweet.strip():
                    return tweet

            return None
        except Exception as e:
            print(f"Error fetching tweet: {e}")
        finally:
            browser.close()
