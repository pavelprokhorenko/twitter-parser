from logging import getLogger
from time import sleep
from typing import Any, Callable

from aiohttp import ClientError

logger = getLogger(__name__)


def safe_request(func: Callable[..., Any]) -> Callable:
    """
    Send request to enabled outer service with delivery guarantee.
    """

    async def wrapper(*args, retries: int = 0, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ClientError as error:
            if retries < 10:
                logger.info("Request was failed. Program pause for 60 seconds.")
                sleep(60)
                return await wrapper(*args, retries=retries + 1, **kwargs)

            raise error

    return wrapper
