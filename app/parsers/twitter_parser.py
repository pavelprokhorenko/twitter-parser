from app.async_client import async_http_client
from app.schemas.tweet import Tweet
from app.schemas.user import TwitterUser
from settings import settings


class TwitterParser:
    """
    Parser that use Twitter API to get data about users.
    """

    def __init__(self):
        self._base_twitter_api_url = "https://api.twitter.com"
        self._headers = {"Authorization": f"Bearer {settings.twitter.api_bearer_token}"}

    async def get_user_data_by_username(self, username: str) -> TwitterUser:
        url = f"{self._base_twitter_api_url}/2/users/by/username/{username}"
        params = {
            "user.fields": ",".join(
                ["id", "name", "username", "description", "public_metrics"]
            )
        }

        user_data = await async_http_client.get(
            url, headers=self._headers, params=params, timeout=5
        )
        user_data = user_data.get("data")

        if not user_data:
            raise ValueError(f"Invalid username {username}")

        user_id = user_data.get("id")
        user = TwitterUser(
            twitter_id=user_id,
            name=user_data.get("name"),
            username=user_data.get("username"),
            description=user_data.get("description"),
            following_count=user_data.get("public_metrics", {}).get("following_count"),
            followers_count=user_data.get("public_metrics", {}).get("followers_count"),
        )
        return user

    async def get_last_tweets(
        self, twitter_id: int, amount_tweets: int = 10
    ) -> list[Tweet]:
        url = f"{self._base_twitter_api_url}/2/users/{twitter_id}/tweets"
        params = {
            "tweet.fields": "id,text,created_at,lang",
            "max_results": amount_tweets,
        }

        if amount_tweets < 5 or amount_tweets > 100:
            raise ValueError("Amount tweets must be between 5 and 100.")

        user_tweets = await async_http_client.get(
            url, headers=self._headers, params=params, timeout=5
        )
        tweets = []
        for tweet in user_tweets.get("data", []):
            tweets.append(
                Tweet(
                    id=tweet.get("id"),
                    text=tweet.get("text"),
                    created_at=tweet.get("created_at"),
                    lang=tweet.get("lang"),
                )
            )

        return tweets


twitter_parser = TwitterParser()
