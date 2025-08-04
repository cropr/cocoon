# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2025

import logging
import httpx
import asyncstdlib as a
import asyncio
from bs4 import BeautifulSoup
from reddevil.core import get_settings
from reddevil.core import RdException, RdNotFound


logger = logging.getLogger(__name__)
clear_cache_started = False
clear_cache_used = False
CACHE_EXPIRES = 300  # Cache expiration time in seconds


@a.cache
async def wagtail_getpages():
    """
    Lists files in Wagtail cms.
    """
    global clear_cache_started, clear_cache_used
    if not clear_cache_started and clear_cache_used:
        clear_cache_started = True
        await clear_cache()  # Start the cache clearing loop
    url = get_settings().WAGTAIL_URL
    retry = 3
    while retry > 0:
        logger.info(
            f"Fetching Wagtail pages from {url}/api/pages/ with {retry} retries left"
        )
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(f"{url}/api/pages/")
                clear_cache_used = True
                return r.json()["items"]
            except httpx.ReadTimeout:
                retry -= 1
                logger.warning(
                    f"Read timeout pages occurred, retrying... {retry} attempts left"
                )
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                )
                raise RdException("Failed to list Wagtail files") from e
        await asyncio.sleep(10)
        continue


async def _wagtail_getpage(id: str) -> dict:
    """
    Get file from Wagtail cms.
    """
    global clear_cache_used
    retry = 3
    url = get_settings().WAGTAIL_URL
    while retry > 0:
        logger.info(
            f"Fetching Wagtail page from {url}/api/pages/{id} with {retry} retries left"
        )
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(f"{url}/api/pages/{id}/")
                clear_cache_used = True
                return r.json()
            except httpx.ReadTimeout:
                retry -= 1
                logger.warning(
                    f"Read timeout page occurred, retrying... {retry} attempts left"
                )
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                )
                raise RdException(f"Failed to get Wagtail file {id}") from e
        await asyncio.sleep(10)
        continue


async def _wagtail_getimage(id: str) -> dict:
    """
    Get image from Wagtail cms.
    """
    global clear_cache_used
    url = get_settings().WAGTAIL_URL
    retry = 3
    while retry > 0:
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(f"{url}/api/images/{id}/")
                clear_cache_used = True
                return r.json()
            except httpx.ReadTimeout:
                retry -= 1
                logger.warning(
                    f"Read timeout image occurred, retrying... {retry} attempts left"
                )
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                )
                raise RdException(f"Failed to get Wagtail image {id}") from e
        await asyncio.sleep(10)
        continue


@a.cache
async def wagtail_getpage(slug: str):
    """
    Get file from Wagtail cms.
    """
    url = get_settings().WAGTAIL_URL
    items = await wagtail_getpages()
    for item in items:
        if item["meta"]["slug"] == slug:
            id = item["id"]
            break
    else:
        raise RdNotFound(f"Wagtail file with slug {slug} not found")
    logger.info(f"Wagtail file {slug} has id {id}")
    doc = await _wagtail_getpage(id)
    body = BeautifulSoup(doc["body"], "html.parser")
    for elem in body:
        if not elem.name == "embed":
            continue
        if elem.get("embedtype") == "image":
            image = await _wagtail_getimage(elem["id"])
            elem.name = "img"
            elem.attrs = {
                "src": f"{url}{image['meta']['download_url']}",
                "class": "img-fluid",
                "alt": image["title"],
                "width": image["width"],
                "height": image["height"],
            }
    doc["body"] = str(body)
    return doc


@a.cache
async def wagtail_getimages():
    """
    Lists files in Wagtail cms.
    """
    global clear_cache_used
    url = get_settings().WAGTAIL_URL
    retry = 3
    while retry > 0:
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(f"{url}/api/images/")
                return r.json()["items"]
            except httpx.ReadTimeout:
                retry -= 1
                logger.warning(
                    f"Read timeout images occurred , retrying... {retry} attempts left"
                )
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                )
                raise RdException("Failed to list Wagtail images") from e


@a.cache
async def wagtail_getimage(title: str):
    """
    Get file from Wagtail cms.
    """
    global clear_cache_used
    items = await wagtail_getimages()
    logger.info(f"wagtail_getimages {items}")
    for item in items:
        if item["title"] == title:
            id = item["id"]
            break
    else:
        raise RdNotFound(f"Wagtail file with title {title} not found")
    logger.info(f"Wagtail image {title} has id {id}")
    doc = await _wagtail_getimage(id)
    return doc


async def clear_cache():
    """
    Clear the Wagtail cache.
    """
    global clear_cache_used
    if not clear_cache_used:
        return
    await asyncio.sleep(CACHE_EXPIRES)
    try:
        wagtail_getpages.cache_clear()
        wagtail_getpage.cache_clear()
        wagtail_getimages.cache_clear()
        wagtail_getimage.cache_clear()
        logger.info("Wagtail cache cleared")
        clear_cache_used = False
    except Exception as e:
        logger.error(f"Failed to clear Wagtail cache: {e}")
        raise RdException("Failed to clear Wagtail cache") from e
    clear_cache_used = False
