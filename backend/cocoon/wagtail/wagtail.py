# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2025

import logging
import httpx
from bs4 import BeautifulSoup
from reddevil.core import get_settings
from reddevil.core import RdException, RdNotFound


logger = logging.getLogger(__name__)


async def wagtail_getpages():
    """
    Lists files in Wagtail cms.
    """
    try:
        url = get_settings().WAGTAIL_URL
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{url}/api/pages/")
            return r.json()["items"]
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        )
        raise RdException("Failed to list Wagtail files") from e


async def wagtail_getpage(slug: str):
    """
    Get file from Wagtail cms.
    """
    try:
        items = await wagtail_getpages()
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
        body = BeautifulSoup(doc["body"], "html.parser")
        logger.info(f"before {body=}")
        for elem in body:
            if not elem.name == "embed":
                continue
            if elem.get("embedtype") == "image":
                async with httpx.AsyncClient() as client:
                    imagestr = await client.get(f"{url}/api/images/{elem['id']}/")
                    logger.info(f"imagestr {imagestr}")
                image = imagestr.json()
                logger.info(f"image {image}")
                elem.name = "img"
                elem.attrs = {
                    "src": f"{url}{image['meta']['download_url']}",
                    "class": "img-fluid",
                    "alt": image["title"],
                    "width": image["width"],
                    "height": image["height"],
                }
        logger.info(f"after {body=}")
        doc["body"] = str(body)
        return doc
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        )
        raise RdException(f"Failed to get Wagtail file {id}") from e


async def wagtail_getimages():
    """
    Lists files in Wagtail cms.
    """
    try:
        url = get_settings().WAGTAIL_URL
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{url}/api/images/")
        return r.json()["items"]
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        )
        raise RdException("Failed to list Wagtail images") from e


async def wagtail_getimage(title: str):
    """
    Get file from Wagtail cms.
    """
    try:
        items = await wagtail_getimages()
        logger.info(f"wagtail_getimages {items}")
        for item in items:
            if item["title"] == title:
                id = item["id"]
                break
        else:
            raise RdNotFound(f"Wagtail file with title {title} not found")
        logger.info(f"Wagtail image {title} has id {id}")
        url = get_settings().WAGTAIL_URL
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{url}/api/images/{id}/")
            return r.json()
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        )
        raise RdException(f"Failed to get Wagtail file {id}") from e
