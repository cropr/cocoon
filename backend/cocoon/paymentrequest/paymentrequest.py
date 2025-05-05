# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, Dict, Any, List
from datetime import date, datetime
from reddevil.core import get_settings
from cocoon.core.mail import MailParams, sendemail_no_attachments

from . import PaymentRequest, PaymentRequestItem, DbPayrequest
from cocoon.core.counter import DbCounter

# from cocoon.core.common import get_common
from cocoon.participant import (
    get_participant,
    get_participants,
    update_participant,
    ParticipantDetail,
    Participant,
)

logger = logging.getLogger(__name__)

settings = get_settings()
# common = get_common()
# i18n = common["i18n"]
# prices = common["prices"]
# startdate = common["period"]["startdate"]
# enddate = common["period"]["enddate"]
# m3y = date(startdate.year - 3, startdate.month, startdate.day)
# m12y = date(startdate.year - 12, startdate.month, startdate.day)
# m18y = date(startdate.year - 18, startdate.month, startdate.day)

# crud


async def create_payment_request(d: Dict[str, Any] = {}) -> str:
    """
    create paymentrequest
    """
    id = await DbPayrequest.add(d)
    return id


async def delete_payment_request(id: str) -> None:
    """
    update paymentrequest
    """
    await DbPayrequest.delete(id)


async def get_payment_request(id: str, options: Dict[str, Any] = {}) -> PaymentRequest:
    """
    get paymentrequest
    """
    filter = options.copy()
    filter["id"] = id
    filter["_model"] = filter.pop("_model", PaymentRequest)
    return cast(PaymentRequest, await DbPayrequest.find_single(filter))


async def get_payment_requests(
    options: Dict[str, Any] = {},
) -> List[PaymentRequestItem]:
    """
    get paymentrequests
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", PaymentRequest)
    if "_fieldlist" not in filter and filter["_model"] != PaymentRequest:
        filter["_fieldlist"] = filter["_model"].__fields__.keys()
    return [cast(PaymentRequest, pr) for pr in await DbPayrequest.find_multiple(filter)]


async def update_payment_request(id: str, pr: PaymentRequest, options={}) -> None:
    """
    update paymentrequest
    """
    opt = options.copy()
    pd = pr.model_dump(exclude_unset=True)
    opt["_model"] = opt.get("_model", PaymentRequest)
    return await DbPayrequest.update(id, pd, opt)


# app routines


def getPaymessage(n) -> str:
    p1, rm = divmod(n, 10000000)
    p2, p3 = divmod(rm, 1000)
    p4 = n % 97 or 97
    return f"+++{p1:03d}/{p2:04d}/{p3:03d}{p4:02d}+++"


async def create_pr_participants() -> str:
    """
    create payrq for all participants without payrq
    """
    ix = 0
    for par in await get_participants({"_model": ParticipantDetail}):
        if par.payment_id:
            continue
        ix += 1
        if ix > 10:
            break
        pr: Dict[str, Any] = {
            "email": par.emailplayer,
            "first_name": par.first_name,
            "last_name": par.last_name,
            "link_id": par.id,
            "locale": par.locale,
            "paystatus": False,
            "reason": "Cocoon 2025",
        }
        pr["details"], pr["totalprice"] = calc_pricedetails_par(par)
        pr["number"] = await DbCounter.next("paymentrequest")
        pr["paymessage"] = getPaymessage(20250000 + pr["number"])
        id = await create_payment_request(pr)
        await update_participant(par.id, Participant(payment_id=id))


async def create_pr_participant(parid: str) -> str:
    """
    create payment request for participant
    """
    par = await get_participant(parid)
    pr: Dict[str, Any] = {
        "email": par.emailplayer,
        "first_name": par.first_name,
        "last_name": par.last_name,
        "link_id": parid,
        "locale": "en",
        "paystatus": False,
        "reason": "Cocoon 2025",
    }
    pr["details"], pr["totalprice"] = calc_pricedetails_par(par)
    pr["number"] = await DbCounter.next("paymentrequest")
    pr["paymessage"] = getPaymessage(20250000 + pr["number"])
    id = await create_payment_request(pr)
    await update_participant(parid, Participant(payment_id=id))
    return id


cutoffdate = datetime(2025, 7, 21, 23, 59, 59)


def calc_pricedetails_par(
    par: ParticipantDetail,
):
    """
    calculates cost for pricedetails
    """
    logger.info(f"Calculation details for participant {par.first_name} {par.last_name}")
    if par.chesstitle in ["GM", "WGM", "IM", "WIM"]:
        amount = 0
    elif par.chesstitle in ["FM", "WFM"]:
        amount = 35
    else:
        amount = 35 if par.birthyear > 2004 else 55
    admincost = 10
    total = amount
    details = [
        {
            "description": f"Registration Cocoon 2025: {par.first_name} {par.last_name}",
            "quantity": 1,
            "unitprice": format(amount, ">6.2f"),
            "totalprice": format(amount, ">6.2f"),
        }
    ]
    logger.info(f"creationtime {par.creationtime}")
    if par.creationtime > cutoffdate:
        logger.info("adding admin cost")
        details.append(
            {
                "description": "Administration cost",
                "quantity": 1,
                "unitprice": format(admincost, ">6.2f"),
                "totalprice": format(admincost, ">6.2f"),
            }
        )
        total += admincost
    return details, total


async def delete_pr_participant(parid: str) -> None:
    par = await get_participant(parid)
    payment_id = par.payment_id
    assert payment_id
    await update_participant(parid, Participant(payment_id=None))
    try:
        await delete_payment_request(payment_id)
    except Exception:
        logger.info("Could not delete linked payment request")
        pass


async def update_pr_participant(id: str, prqin: PaymentRequest) -> None:
    exprq = await get_payment_request(id)
    par = await get_participant(exprq.link_id)
    logger.info(f"updating par {par}")
    (details, totalprice) = calc_pricedetails_par(par)
    prqdict = prqin.model_dump(exclude_unset=True)
    prqdict["details"] = details
    prqdict["totalprice"] = totalprice
    await DbPayrequest.update(id, prqdict, {"_model": PaymentRequest})


async def email_paymentrequest(prqid) -> None:
    prq = await get_payment_request(prqid)
    assert prq.email and prq.locale
    mp = MailParams(
        subject="Payment Cocoon 2025",
        sender=settings.EMAIL["sender"],
        receiver=prq.email,
        template="pr_part_mail.md",
        locale=prq.locale,
        attachments=[],
        bcc=settings.EMAIL.get("bcc_registration", ""),
    )
    sendemail_no_attachments(mp, prq.model_dump(), "paymentrq participant")
    await update_payment_request(
        prqid, PaymentRequest(sentdate=date.today().isoformat())
    )


async def email_paymentrequests(prqid) -> None:
    """
    send all virgin payment requests
    """
    prqs = await get_payment_requests()
    for prq in prqs:
        if prq.sentdate:
            continue
        await email_paymentrequest(prq.id)
