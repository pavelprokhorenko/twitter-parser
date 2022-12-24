from fastapi import APIRouter, Path, Query, status

from app.parsers.twitter_parser import twitter_parser
from app.schemas import Tweet

router = APIRouter()


@router.get("/{twitter_id}", status_code=status.HTTP_200_OK, response_model=list[Tweet])
async def get_last_tweets(
    twitter_id: int = Path(...), amount_tweets: int | None = Query(default=10)
) -> list[Tweet]:
    """
    Get last tweets from Twitter user with given id.
    """
    return await twitter_parser.get_last_tweets(
        twitter_id=twitter_id, amount_tweets=amount_tweets
    )
