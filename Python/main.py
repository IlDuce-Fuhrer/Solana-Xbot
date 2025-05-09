import requests
from bs4 import BeautifulSoup


def get_latest_tweet(username):
    url = f"https://twitter.com/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch page")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        tweets = soup.find_all("div", {"data-testid": "tweet"})

        if not tweets:
            return None

        latest = tweets[0].get_text()
        return latest

    except Exception as e:
        print(f"Error: {e}")
        return None


# Example usage
if __name__ == "__main__":
    tweet = get_latest_tweet("elonmusk")
    print("Latest tweet:", tweet)
