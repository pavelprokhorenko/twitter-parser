from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models.user import ParseUserStatuses
from app.parsers.twitter_parser import twitter_parser


async def parse_users(db: AsyncSession, *, users: list[dict[str, Any]]) -> None:
    """
    Shortcut for multiple parsing Twitter users into database.
    """

    for user in users:
        try:
            user_data = await twitter_parser.get_user_data_by_username(user["username"])
            status = ParseUserStatuses.SUCCESS.name
        except ValueError:
            user_data = {}
            status = ParseUserStatuses.FAILED.name

        user_in = {"parse_status": status, **user_data.dict(exclude_unset=True)}
        await crud.user.update(db, pk=user["id"], obj_in=user_in)
