# poll_and_respond.py

import asyncio
from monitor import fetch_latest_tweet

TARGET_USERNAME = "dulc1x"  # Change to your desired account

def is_valid_command(tweet):
    # Detect if tweet is a command like "@YourBot SEND 1 SOL TO ..."
    return tweet and "@YourBot" in tweet and "SEND" in tweet

async def main():
    print("Starting tweet monitor...")
    while True:
        tweet = await fetch_latest_tweet(TARGET_USERNAME)
        if tweet:
            print("Latest tweet:", tweet)
            if is_valid_command(tweet):
                print("✅ Detected valid command! Triggering Solana transaction...")
                # Call your solana transaction function here
        else:
            print("No new tweet or tweet unchanged.")
        await asyncio.sleep(30)  # Wait 30 seconds between polls

asyncio.run(main())
