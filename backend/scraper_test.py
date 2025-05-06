from playwright.sync_api import sync_playwright

def get_latest_tweet(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # For debugging, set to True later
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/119.0.0.0 Safari/537.36"
        ))
        page = context.new_page()
        try:
            page.goto(f"https://twitter.com/{username}", timeout=900000)
            page.wait_for_selector("article", timeout=85000)
            tweet = page.query_selector("article div[lang]")
            if tweet:
                text = tweet.inner_text()
                print(f"Latest tweet from @{username}: {text}")
                return text
            else:
                print("No tweet found.")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            browser.close()

# Example usage
if __name__ == "__main__":
    get_latest_tweet("oluwaseyi__7")
