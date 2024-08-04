# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, Dict, Any, List
from datetime import date, datetime
from reddevil.core import get_settings
from cocoon.core.mail import MailParams, sendemail_no_attachments

from . import PaymentRequest, PaymentRequestItem, DbPayrequest
from cocoon.core.counter import DbCounter
from cocoon.core.common import get_common
from cocoon.participant import (
    get_participant_bjk,
    get_participant_vk,
    get_participants_bjk,
    get_participants_vk,
    update_participant_bjk,
    update_participant_vk,
    ParticipantBJKDetail,
    ParticipantVKDetail,
    ParticipantBJK,
    ParticipantVK,
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
i18n_enrollment_vk = {
    "nl": "Inschrijving VK2024",
    "en": "Enrollment VK2024",
}
i18n_enrollment_bjk = {
    "nl": "Inschrijving BJK 2024",
    "en": "Enrollment BYCC 2024",
    "fr": "Enregistrement CBJ 2024",
    "de": "Anmeldung BJLM 2024",
}
i18n_administrative_cost = {
    "nl": "Extra adminstratiekosten",
    "en": "Additional administration costs",
    "fr": "Frais administratifs supplémentaires",
    "de": "Zusätzliche Verwaltungskosten",
}

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
    options: Dict[str, Any] = {}
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


# participant vk


async def create_pr_participants_vk() -> str:
    """
    create payrq for all participants wihtout payrq
    """
    ix = 0
    for par in await get_participants_vk({"_model": ParticipantVKDetail}):
        if par.payment_id:
            continue
        ix += 1
        if ix > 10:
            break
        pr: Dict[str, Any] = {
            "email": ",".join(par.emails),
            "first_name": par.first_name,
            "last_name": par.last_name,
            "link_id": par.id,
            "locale": par.locale,
            "paystatus": False,
            "reason": "vk2024",
        }
        pr["details"], pr["totalprice"] = calc_pricedetails_par_vk(par)
        pr["number"] = await DbCounter.next("paymentrequest")
        pr["paymessage"] = getPaymessage(20240000 + pr["number"])
        id = await create_payment_request(pr)
        await update_participant_vk(par.id, ParticipantVK(payment_id=id))


async def create_pr_participant_vk(parid: str) -> str:
    """
    create a single payment request for a participant
    """
    par = await get_participant_vk(parid)
    pr: Dict[str, Any] = {
        "email": ",".join(par.emails),
        "first_name": par.first_name,
        "last_name": par.last_name,
        "link_id": parid,
        "locale": par.locale,
        "paystatus": False,
        "reason": "vk2024",
    }
    pr["details"], pr["totalprice"] = calc_pricedetails_par_vk(par)
    pr["number"] = await DbCounter.next("paymentrequest")
    pr["paymessage"] = getPaymessage(20240000 + pr["number"])
    id = await create_payment_request(pr)
    await update_participant_vk(parid, ParticipantVK(payment_id=id))
    return id


def calc_pricedetails_par_vk(
    par: ParticipantVKDetail,
):
    """
    calculates cost for pricedetails
    """
    amount = 50
    if par.chesstitle:
        if par.chesstitle in ["WFM", "FM"]:
            amount = 25
        if par.chesstitle in ["WIM", "IM", "GM", "WGM"]:
            amount = 0
    if par.locale not in ["en", "nl"]:
        par.locale = "en"
    details = [
        {
            "description": i18n_enrollment_vk[par.locale],
            "quantity": 1,
            "unitprice": format(amount, ">6.2f"),
            "totalprice": format(amount, ">6.2f"),
        }
    ]
    return details, amount


async def delete_pr_participant_vk(parid: str) -> None:
    par = await get_participant_vk(parid)
    payment_id = par.payment_id
    assert payment_id
    await update_participant_vk(parid, ParticipantVK(payment_id=None))
    try:
        await delete_payment_request(payment_id)
    except:
        logger.info("Could not delete linked payment request")
        pass


async def update_pr_participant_vk(id: str, prqin: PaymentRequest) -> None:
    exprq = await get_payment_request(id)
    par = await get_participant_vk(exprq.link_id)
    (details, totalprice) = calc_pricedetails_par_vk(
        par, prqin.reductionamount, prqin.reductionpct
    )
    prqdict = prqin.model_dump(exclude_unset=True)
    prqdict["details"] = details
    prqdict["totalprice"] = totalprice
    await DbPayrequest.update(id, prqdict, {"_model": PaymentRequest})


async def email_pr_participant_vk(prqid) -> None:
    prq = await get_payment_request(prqid)
    assert prq.email and prq.locale
    if prq.locale not in ["en", "nl"]:
        prq.locale = "en"
    mp = MailParams(
        subject="VK 2024",
        sender=settings.EMAIL["sender"],
        receiver=prq.email,
        template="pr_part_vk_mail_{locale}.md",
        locale=prq.locale,
        attachments=[],
        bcc=settings.EMAIL["bcc_enrollment"],
    )
    sendemail_no_attachments(mp, prq.model_dump(), "paymentrq participant vk")
    await update_payment_request(
        prqid, PaymentRequest(sentdate=date.today().isoformat())
    )


# participant bjk


async def create_pr_participants_bjk() -> str:
    """
    create payrq for all participants wihtout payrq
    """
    ix = 0
    for par in await get_participants_bjk({"_model": ParticipantBJKDetail}):
        if par.payment_id:
            continue
        ix += 1
        if ix > 10:
            break
        pr: Dict[str, Any] = {
            "email": ",".join(par.emails),
            "first_name": par.first_name,
            "last_name": par.last_name,
            "link_id": par.id,
            "locale": par.locale,
            "paystatus": False,
            "reason": "bjk2024",
        }
        pr["details"], pr["totalprice"] = calc_pricedetails_par_bjk(par)
        pr["number"] = await DbCounter.next("paymentrequest")
        pr["paymessage"] = getPaymessage(20240000 + pr["number"])
        id = await create_payment_request(pr)
        await update_participant_bjk(par.id, ParticipantVK(payment_id=id))


async def create_pr_participant_bjk(parid: str) -> str:
    """
    create payment request for participant
    """
    par = await get_participant_bjk(parid)
    pr: Dict[str, Any] = {
        "email": ",".join(par.emails),
        "first_name": par.first_name,
        "last_name": par.last_name,
        "link_id": parid,
        "locale": par.locale,
        "paystatus": False,
        "reason": "bjk2024",
    }
    pr["details"], pr["totalprice"] = calc_pricedetails_par_bjk(par)
    pr["number"] = await DbCounter.next("paymentrequest")
    pr["paymessage"] = getPaymessage(20240000 + pr["number"])
    id = await create_payment_request(pr)
    await update_participant_bjk(parid, ParticipantVK(payment_id=id))
    return id


def calc_pricedetails_par_bjk(
    par: ParticipantBJKDetail,
):
    """
    calculates cost for pricedetails
    """
    amount = 35
    admincost = 10
    total = amount
    details = [
        {
            "description": i18n_enrollment_bjk[par.locale],
            "quantity": 1,
            "unitprice": format(amount, ">6.2f"),
            "totalprice": format(amount, ">6.2f"),
        }
    ]
    logger.info(f"par._creationtime")
    if par.creationtime > datetime(2024, 4, 20):
        logger.info("adding admin cost")
        details.append(
            {
                "description": i18n_administrative_cost[par.locale],
                "quantity": 1,
                "unitprice": format(admincost, ">6.2f"),
                "totalprice": format(admincost, ">6.2f"),
            }
        )
        total += admincost
    return details, total


async def delete_pr_participant_bjk(parid: str) -> None:
    par = await get_participant_bjk(parid)
    payment_id = par.payment_id
    assert payment_id
    await update_participant_bjk(parid, ParticipantVK(payment_id=None))
    try:
        await delete_payment_request(payment_id)
    except:
        logger.info("Could not delete linked payment request")
        pass


async def update_pr_participant_bjk(id: str, prqin: PaymentRequest) -> None:
    exprq = await get_payment_request(id)
    par = await get_participant_bjk(exprq.link_id)
    logger.info(f"updating par {par}")
    (details, totalprice) = calc_pricedetails_par_bjk(par)
    prqdict = prqin.model_dump(exclude_unset=True)
    prqdict["details"] = details
    prqdict["totalprice"] = totalprice
    await DbPayrequest.update(id, prqdict, {"_model": PaymentRequest})


async def email_pr_participant_bjk(prqid) -> None:
    prq = await get_payment_request(prqid)
    assert prq.email and prq.locale
    mp = MailParams(
        subject="BJK / CBJ / BJLM 2024",
        sender=settings.EMAIL["sender"],
        receiver=prq.email,
        template="pr_part_bjk_mail_{locale}.md",
        locale=prq.locale,
        attachments=[],
        bcc=settings.EMAIL["bcc_enrollment"],
    )
    sendemail_no_attachments(mp, prq.model_dump(), "paymentrq participant bjk")
    await update_payment_request(
        prqid, PaymentRequest(sentdate=date.today().isoformat())
    )


# more general

emailfunctions = {
    "vk2024": email_pr_participant_vk,
    "bjk2024": email_pr_participant_bjk,
}


async def email_paymentrequest(prqid) -> None:
    prq = await get_payment_request(prqid)
    if prq.reason in emailfunctions:
        await emailfunctions[prq.reason](prqid)
    else:
        logger.info(f"reason not implemented: {prq.reason}")
        raise NotImplemented


async def email_paymentrequests(prqid) -> None:
    """
    send all virgin payment requests
    """
    prqs = await get_payment_requests()
    for prq in prqs:
        if prq.sentdate:
            continue
        if prq.reason in emailfunctions:
            await emailfunctions[prq.reason](prq.id)
        else:
            logger.info(f"reason not implemented: {prq.reason}")
            raise NotImplemented
