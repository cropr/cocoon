# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, APIRouter

# from fastapi.security import HTTPAuthorizationCredentials
from reddevil.core import RdException, bearer_schema, validate_token

from . import checkin, checkout


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/page")


# # test endpoints


# @router.post("/checkin/{st_instance}", status_code=201)
# async def api_checkin(
#     st_instance: str,
#     # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
# ):
#     try:
#         # await validate_token(auth)
#         await checkin(st_instance)
#     except RdException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.description)
#     except:
#         logger.exception("failed api call bucket_to_statamic")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/checkout", status_code=201)
async def api_statamic_to_bucket(
    # auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        # await validate_token(auth)
        await checkout()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call statamic_to_bucket")
        raise HTTPException(status_code=500, detail="Internal Server Error")
