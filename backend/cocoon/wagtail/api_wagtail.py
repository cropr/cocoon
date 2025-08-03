# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, APIRouter

from reddevil.core import RdException

from .wagtail import (
    wagtail_getpages,
    wagtail_getpage,
    wagtail_getimages,
    wagtail_getimage,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/wagtail")


@router.get("/pages")
async def api_wagtail_getpages():  # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),  try:
    try:
        return await wagtail_getpages()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call wagtail_getpages")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/pages/{slug}")
async def api_wagtail_getpage(slug: str):
    try:
        return await wagtail_getpage(slug)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call wagtail_getpage")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/images")
async def api_wagtail_getimages():  # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),  try:
    try:
        return await wagtail_getimages()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call wagtail_getimages")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/images/{title}")
async def api_wagtail_getimage(title: str):
    try:
        return await wagtail_getimage(title)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call wagtail_getimage")
        raise HTTPException(status_code=500, detail="Internal Server Error")
