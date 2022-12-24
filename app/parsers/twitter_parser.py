from app.async_client import async_http_client
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
        params = {"user.fields": "id,name,username,description"}

        user_data = await async_http_client.get(
            url, headers=self._headers, params=params
        )
        if not user_data:
            raise ValueError(f"Invalid username {username}")

        user_data = user_data.get("data")
        user_id = user_data.get("id")
        user = TwitterUser(
            twitter_id=user_id,
            name=user_data.get("name"),
            username=user_data.get("username"),
            description=user_data.get("description"),
            following_count=await self._get_user_following_count(user_id),
            followers_count=await self._get_user_followers_count(user_id),
        )
        return user

    async def _get_user_following_count(self, user_id: int) -> int:
        url = f"{self._base_twitter_api_url}/1.1/friends/ids.json"
        params = {"user_id": user_id, "count": 5000}
        following_count = 0

        user_following_ids = await async_http_client.get(
            url, headers=self._headers, params=params
        )

        while user_following_ids:
            following_count += len(user_following_ids.get("ids", []))

            params["cursor"] = user_following_ids.get("next_cursor")
            user_following_ids = await async_http_client.get(
                url, headers=self._headers, params=params
            )

        return following_count

    async def _get_user_followers_count(self, user_id: int) -> int:
        url = f"{self._base_twitter_api_url}/1.1/followers/ids.json"
        params = {"user_id": user_id, "count": 5000}
        following_count = 0

        user_following_ids = await async_http_client.get(
            url, headers=self._headers, params=params
        )
        while user_following_ids:
            following_count += len(user_following_ids.get("ids", []))

            params["cursor"] = user_following_ids.get("next_cursor")
            user_following_ids = await async_http_client.get(
                url, headers=self._headers, params=params
            )

        return following_count


twitter_parser = TwitterParser()
