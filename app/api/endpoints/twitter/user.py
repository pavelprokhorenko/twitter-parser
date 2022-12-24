from fastapi import APIRouter, Path, status

from app.parsers.twitter_parser import twitter_parser
from app.schemas.user import TwitterUser

router = APIRouter()


@router.get("/{username}", status_code=status.HTTP_200_OK, response_model=TwitterUser)
async def get_twitter_user_by_username(username: str = Path(...)) -> TwitterUser:
    """
    Get data about Twitter user with given username.
    """
    return await twitter_parser.get_user_data_by_username(username)
