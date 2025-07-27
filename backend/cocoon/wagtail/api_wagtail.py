# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, APIRouter

from reddevil.core import RdException

from .wagtail import list_wagtail_files, get_wagtail_file

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/wagtail")


@router.get("/")
async def api_wagtail_list():  # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),  try:
    try:
        return await list_wagtail_files()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call wagtail_lis")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{slug}")
async def api_wagtail_get(slug: str):
    try:
        return await get_wagtail_file(slug)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call wagtail_get")
        raise HTTPException(status_code=500, detail="Internal Server Error")
