# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2025

import logging
import httpx
from reddevil.core import get_settings
from reddevil.core import RdException, RdNotFound


logger = logging.getLogger(__name__)


async def list_wagtail_files():
    """
    Lists files in Wagtail cms.
    """
    try:
        url = get_settings().WAGTAIL_URL
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{url}/api/pages/")
            items = r.json()["items"]
        return items
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        )
        raise RdException("Failed to list Wagtail files") from e


async def get_wagtail_file(slug: str):
    """
    Get file from Wagtail cms.
    """
    try:
        items = await list_wagtail_files()
        for item in items:
            if item["meta"]["slug"] == slug:
                id = item["id"]
                break
        else:
            raise RdNotFound(f"Wagtail file with slug {slug} not found")
        logger.info(f"Wagtail file {slug} has id {id}")
        url = get_settings().WAGTAIL_URL
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{url}/api/pages/{id}/")
            doc = r.json()
        return doc
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        )
        raise RdException(f"Failed to get Wagtail file {id}") from e
