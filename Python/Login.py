# login_once.py
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="user_data",  # This folder stores session
            headless=False
        )
        page = await browser.new_page()
        await page.goto("https://twitter.com/login")

        print("Log in to your Twitter account manually, then close the browser.")
        await page.wait_for_timeout(60000 * 5)  # Wait 5 minutes max

        await browser.close()

asyncio.run(main())
