# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from typing import List
from fastapi import HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, Response
from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema
from reddevil.core import validate_token

from . import (
    ParticipantItem,
    ParticipantDetail,
    ParticipantUpdate,
    # generate_badges,
    # generate_namecards,
    # generate_prizes,
    get_participants,
    get_participant,
    get_photo,
    import_registrations,
    update_elo,
    update_participant,
    upload_photo,
)


router = APIRouter(prefix="/api/v1/participant")
logger = logging.getLogger(__name__)


@router.get("/list", response_model=List[ParticipantItem])
async def api_get_participants(enabled: str | None = None):
    try:
        if enabled:
            return await get_participants({"enabled": True})
        else:
            return await get_participants()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_particpants")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/single/{id}", response_model=ParticipantDetail)
async def api_mgmt_get_participant(
    id: str, auth: HTTPAuthorizationCredentials = Depends(bearer_schema)
):
    try:
        # await validate_token(auth)
        return await get_participant(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_particpant")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/single/{id}", response_model=ParticipantDetail)
async def api_mgmt_update_participant(
    id: str,
    participant: ParticipantUpdate,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await update_participant(id, participant)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call update_participant")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/import_registrations", status_code=201)
async def api_mgmt_import_registrations(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    logger.info("API participants")
    try:
        await validate_token(auth)
        await import_registrations()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call mgmt_import_registrations")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/update/elo/", status_code=201)
async def api_mgmt_update_elo(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        await update_elo()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call mgmt_update_elo_vk")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.get("/namecards_cat/{cat}", response_class=HTMLResponse)
# async def api_generate_namecards_cat(cat: str):
#     try:
#         return await generate_namecards(cat)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except Exception:
#         logger.exception("failed api call generate_namecards")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get("/namecards_id/{ids}", response_class=HTMLResponse)
# async def api_generate_namecards_ids(ids: str):
#     try:
#         return await generate_namecards(cat="", ids=ids)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except Exception:
#         logger.exception("failed api call generate_namecards")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get("/badges_cat/{cat}", response_class=HTMLResponse)
# async def api_generate_badges_cat(cat: str):
#     try:
#         return await generate_badges(cat)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except Exception:
#         logger.exception("failed api call generate_namecards")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get("/badges_id//{ids}", response_class=HTMLResponse)
# async def api_generate_badges_ids(ids: str):
#     try:
#         return await generate_badges(cat="", ids=ids)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except Exception:
#         logger.exception("failed api call generate_namecards")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/photo/{id}", response_class=Response)
async def api_get_photo(id: str):
    try:
        return await get_photo(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_participant")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/photo/{id}")
async def api_upload_photo(id: str, body: dict):
    try:
        return await upload_photo(id, body["photo"])
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call upload_photo")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.get("/prizes/", response_class=HTMLResponse)
# async def api_generate_prizes():
#     try:
#         return await generate_prizes()
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except Exception:
#         logger.exception("failed api call generate_prizes")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
