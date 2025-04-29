# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast
from datetime import datetime
from fastapi import BackgroundTasks
from fastapi.responses import Response
from binascii import a2b_base64
from httpx import AsyncClient, DecodingError, TransportError

from reddevil.core import get_settings, RdBadRequest, RdNotFound
from cocoon.registration import (
    DbRegistration,
    Registration,
    RegistrationIn,
    RegistrationItem,
    RegistrationUpdate,
    IdReply,
)


logger = logging.getLogger(__name__)

api_lookupbel = "/api/v1/member/anon/member/{id}"
api_lookupfide = "/api/v1/member/anon/fidemember/{id}"
api_fideis2belid = "/api/v1/member/anon/fideid2belid/{id}"

# crud operations


async def add_registration(edict: dict) -> str:
    """
    add an enrollment
    """
    id = await DbRegistration.add(edict)
    return id


async def get_registrations(options: dict = None) -> list[RegistrationItem]:
    """
    get enrollments
    """
    filter = options.copy() if options else {}
    filter["_model"] = filter.pop("_model", RegistrationItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    return [
        cast(RegistrationItem, x) for x in await DbRegistration.find_multiple(filter)
    ]


async def get_registration(id: str, options: dict | None = None) -> RegistrationItem:
    """
    get enrollments
    """
    filter = options.copy() if options else {}
    filter["_model"] = filter.pop("_model", RegistrationItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["id"] = id
    reg = cast(RegistrationItem, await DbRegistration.find_single(filter))
    return reg


async def update_registration(
    id: str, eu: RegistrationUpdate, options: dict = {}
) -> Registration:
    """
    update an enrollment
    """
    filter = options.copy()
    filter["_model"] = filter.pop("_model", Registration)
    eudict = eu.model_dump(exclude_unset=True)
    mo = cast(
        Registration,
        await DbRegistration.update(id, eudict, filter),
    )
    mo.badgeimage = None
    return mo


# business methods


async def create_registration(ei: RegistrationIn) -> str:
    logger.info(f"create an registration for Cocoon {ei}")

    if ei.idsub:
        eu = RegistrationUpdate(
            category=ei.category,
            emailplayer=ei.emailplayer,
            idbel=ei.idbel,
            idfide=ei.idfide,
            locale=ei.locale,
            mobileplayer=ei.mobileplayer,
        )
        enrid = (await update_registration(ei.idsub, eu)).id
    else:
        eidict = ei.model_dump()
        eidict.pop("idsub", None)
        eidict["event"] = ""
        enrid = await add_registration(eidict)
    meu = RegistrationUpdate()
    if ei.idbel:
        try:
            pl = await lookup_idbel(ei.idbel)
            meu.birthyear = pl.birthyear
            meu.gender = pl.gender
            meu.first_name = pl.first_name
            meu.idclub = pl.idclub
            meu.last_name = pl.last_name
            meu.nationalitybel = pl.nationalitybel
            meu.ratingbel = pl.ratingbel
        except Exception as e:
            logger.info(f"lookup idbel failed {e}")
    if ei.idfide:
        try:
            pl = await lookup_idfide(ei.idfide)
            meu.birthyear = pl.birthyear
            meu.gender = pl.gender
            meu.first_name = pl.first_name
            meu.last_name = pl.last_name
            meu.nationalityfide = pl.nationalityfide
            meu.ratingfide = pl.ratingfide
        except Exception as e:
            logger.info(f"lookup idfide failed {e}")
    await update_registration(enrid, meu)
    return enrid


async def lookup_idbel(idbel: str) -> IdReply:
    """
    lookup member by idbel in KBSB member directory
    """
    settings = get_settings()
    url = api_lookupbel.format(id=idbel)
    try:
        async with AsyncClient() as client:
            rc = await client.get(f"{settings.KBSB_HOST}{url}")
            plyr = rc.json()
    except DecodingError:
        raise RdBadRequest("DecodingErrorKBSB")
    except TransportError:
        raise RdBadRequest("TransportErrorKBSB")
    if rc.status_code != 200:
        logger.info(f"failed api call to kbsb lookup_idbel {rc}")
        raise RdNotFound(description="FailedApiKBSB")
    return IdReply(
        belfound=True,
        birthyear=plyr["birthyear"],
        first_name=plyr["first_name"],
        gender=plyr["gender"],
        idbel=idbel,
        idclub=str(plyr["idclub"] or 0),
        idfide=str(plyr["idfide"] or 0),
        last_name=plyr["last_name"],
        nationalitybel=plyr["nationalitybel"],
        nationalityfide=plyr["nationalityfide"],
        ratingbel=plyr["natrating"],
        ratingfide=plyr["fiderating"],
        subconfirmed=False,
        subid=None,
    )


async def lookup_idfide(idfide: str) -> IdReply:
    settings = get_settings()
    # first see if we have a bel id for the
    url = api_fideis2belid.format(id=idfide)
    try:
        async with AsyncClient() as client:
            rc = await client.get(f"{settings.KBSB_HOST}{url}")
            if rc.status_code == 200 and rc.text and rc.text != "0":
                idbel = rc.text
                belreply = await lookup_idbel(idbel)
            else:
                idbel = ""
                belreply = None
    except DecodingError:
        raise RdBadRequest(description="DecodingErrorKBSB")
    except TransportError:
        raise RdBadRequest(description="TransportErrorKBSB")
    url = api_lookupfide.format(id=idfide)
    try:
        async with AsyncClient() as client:
            rc = await client.get(f"{settings.KBSB_HOST}{url}")
            plyr = rc.json()
    except DecodingError:
        raise RdBadRequest("DecodingErrorKBSB")
    except TransportError:
        raise RdBadRequest("TransportErrorKBSB")
    if rc.status_code != 200:
        logger.info(f"failed api call to kbsb lookup_idfide {rc}")
        raise RdNotFound(description="FailedApiKBSB")
    reply = IdReply(
        belfound=belreply is not None,
        birthyear=plyr["birthyear"],
        chesstitle=plyr.get("chesstitle", ""),
        first_name=plyr["first_name"],
        gender=plyr["gender"],
        idbel=idbel,
        idclub="",
        idfide=idfide,
        last_name=plyr["last_name"],
        nationalitybel=belreply.nationalitybel if belreply else "",
        nationalityfide=plyr["nationalityfide"],
        ratingbel=belreply.ratingbel if belreply else 0,
        ratingfide=plyr["fiderating"],
        subconfirmed=False,
        subid=None,
    )
    return reply


async def upload_photo(id: str, photo: str) -> None:
    try:
        header, data = photo.split(",")
        imagedata = a2b_base64(data)
        su = RegistrationUpdate(
            badgemimetype=header.split(":")[1].split(";")[0],
            badgeimage=imagedata,
            badgelength=len(cast(str, imagedata)),
        )
    except Exception:
        raise RdBadRequest(description="BadPhotoData")
    await update_registration(id, su)


async def confirm_registration(id: str, bt: BackgroundTasks) -> None:
    su = RegistrationUpdate(
        confirmed=True, registrationtime=datetime.now(), enabled=True
    )
    enr = await update_registration(id, su)
    sendemail_registration(enr)


async def get_photo(id: str):
    photo = await DbRegistration.find_single(
        {
            "id": id,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])


def sendemail_registration(reg: Registration) -> None:
    from cocoon.core.mail import MailParams, sendemail_no_attachments

    settings = get_settings()
    emails = [reg.emailplayer]
    mp = MailParams(
        subject="Registration Cocoon 2025",
        sender=settings.EMAIL["sender"],
        receiver=",".join(emails),
        template="mailregistration_en.md",
        locale=reg.locale,
        attachments=[],
        bcc=settings.EMAIL.get("bcc_registration"),
    )
    edict = reg.model_dump()
    edict["category"] = edict["category"].value
    sendemail_no_attachments(mp, edict, "confirmation enrollment")


def sendemail_confirmationreq(enr: Registration) -> None:
    from cocoon.core.mail import MailParams, sendemail_no_attachments

    settings = get_settings()
    emails = [enr.emailplayer]
    mp = MailParams(
        subject="Payment Cocoon 2025",
        sender=settings.EMAIL["sender"],
        receiver=",".join(emails),
        template="mailenrollment_vk_{locale}.md",
        locale=enr.locale,
        attachments=[],
        bcc=settings.EMAIL.get("bcc_registration"),
    )
    edict = enr.model_dump()
    edict["category"] = edict["category"].value
    sendemail_no_attachments(mp, edict, "confirmation enrollment")


async def send_notconfirmed() -> None:
    """
    get a list of all enrollments of an event that are not confirmed
    and sends a requestConfirmation email to them
    """
    for enr in await get_registrations(
        {
            "confirmed": {"$eq": None},
            "enabled": True,
            "confirmation_email": {"$eq": None},
        }
    ):
        pass
