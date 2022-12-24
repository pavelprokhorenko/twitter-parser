from fastapi import APIRouter, BackgroundTasks, Body, Depends, Path, Query, status
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.deps import get_db_pg
from app.models.user import ParseUserStatuses
from app.parsers.twitter_parser import twitter_parser
from app.schemas import ParseUsers, ParsingSession, TwitterUser
from app.utils.twitter import parse_users

router = APIRouter()


@router.get("/status", status_code=status.HTTP_200_OK, response_model=list[ParseUsers])
async def get_parsing_status(
    session_id: int = Query(...), db: AsyncSession = Depends(get_db_pg)
) -> list[ParseUsers]:
    """
    Get parsing status for each user in the session.
    """
    parsing_users = []
    users = await crud.user.get_all(db, session_id=session_id)

    for user in users:
        parsing_users.append(
            ParseUsers(username=user.username, status=user.parse_status)
        )

    return parsing_users


@router.get("/{username}", status_code=status.HTTP_200_OK, response_model=TwitterUser)
async def get_twitter_user_by_username(username: str = Path(...)) -> TwitterUser:
    """
    Get data about Twitter user with given username.
    """
    return await twitter_parser.get_user_data_by_username(username)


@router.post("/", status_code=status.HTTP_200_OK, response_model=ParsingSession)
async def parse_twitter_users(
    *,
    account_urls: list[HttpUrl] = Body(...),
    db: AsyncSession = Depends(get_db_pg),
    background_tasks: BackgroundTasks
) -> dict[str, int]:
    """
    Parse users from Twitter.
    """
    users = []  # [{"id": int, "username": str}]
    session = await crud.parsing_session.create(db, obj_in={})

    for account_url in account_urls:
        account_username = account_url.split("/")[-1]

        pending_user_data = {
            "username": account_username,
            "parse_status": ParseUserStatuses.PENDING.name,
            "session_id": session.id,
        }
        pending_user = await crud.user.create(db, obj_in=pending_user_data)
        users.append({"id": pending_user.id, "username": pending_user.username})

    background_tasks.add_task(parse_users, db=db, users=users)
    return {"session_id": session.id}
