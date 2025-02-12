# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2020

import logging
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import HTTPAuthorizationCredentials
from typing import List
from reddevil.core import RdException, get_settings, bearer_schema, validate_token

from cocoon.main import app
from . import (
    create_pr_participant,
    create_pr_participants,
    delete_pr_participant,
    email_paymentrequest,
    email_paymentrequests,
    get_payment_requests,
    get_payment_request,
    update_payment_request,
    update_pr_participant,
    PaymentRequest,
    PaymentRequestItem,
)


logger = logging.getLogger("cocoon")
router = APIRouter(prefix="/api/v1/payment")
settings = get_settings()

# general


@router.get("/pr/{prqid}", response_model=PaymentRequest)
async def api_mgmt_get_paymentrequest(
    prqid: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await get_payment_request(prqid)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/pr", response_model=List[PaymentRequestItem])
async def api_mgmt_get_paymentrequests(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    logger.info("XXX")
    try:
        await validate_token(auth)
        return await get_payment_requests()
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call get_payment_request")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/pr/{id}", response_model=PaymentRequest)
async def api_update_paymentrequest(
    id: str,
    prq: PaymentRequest,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await update_payment_request(id, prq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call update payment_request")
        raise HTTPException(status_code=500)


@router.post("/email_pr/{id}")
async def api_email_paymentrequest(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await email_paymentrequest(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.post("/email_pr")
async def api_email_paymentrequests(
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await email_paymentrequests(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call create_pr_reservation")
        raise HTTPException(status_code=500)


@router.post("/participant_pr/{id}", response_model=str)
async def api_create_pr_participant(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        return await create_pr_participant(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call api_create_pr_participant")
        raise HTTPException(status_code=500)


@router.put("/participant_pr/{id}")
async def api_update_pr_participant(
    id: str,
    prq: PaymentRequest,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await update_pr_participant(id, prq)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call update_pr_reservation")
        raise HTTPException(status_code=500)


@router.delete("/participant_pr/{id}")
async def api_delete_pr_participant(
    id: str,
    auth: HTTPAuthorizationCredentials = Depends(bearer_schema),
):
    try:
        await validate_token(auth)
        await delete_pr_participant(id)
    except RdException as e:
        raise HTTPException(status_code=e.status_code, detail=e.description)
    except Exception:
        logger.exception("failed api call delete_pr_reservation")
        raise HTTPException(status_code=500)
