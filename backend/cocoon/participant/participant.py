# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging
from typing import cast, List, Dict, Any
from binascii import a2b_base64
from fastapi import Response
from jinja2 import FileSystemLoader, Environment

from reddevil.core import RdBadRequest, RdNotFound

from . import (
    ParticipantCategory,
    ParticipantDetail,
    ParticipantItem,
    ParticipantUpdate,
    Participant,
    DbParticpant,
    Gender,
)
from cocoon.registration import (
    Registration,
    get_registration,
    get_registrations,
    lookup_idbel,
    lookup_idfide,
)

logger = logging.getLogger(__name__)
env = Environment(loader=FileSystemLoader("cocoon/templates"), trim_blocks=True)


async def get_participants(options: dict | None = None) -> List[ParticipantItem]:
    filter = options.copy() if options else {}
    filter["_model"] = filter.pop("_model", ParticipantItem)
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["_fieldlist"].append("_creationtime")
    return [cast(ParticipantItem, x) for x in await DbParticpant.find_multiple(filter)]


async def get_participant(id: str) -> ParticipantDetail:
    filter = {"_model": ParticipantDetail}
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["_fieldlist"].append("_creationtime")
    filter["id"] = id
    par = await DbParticpant.find_single(filter)
    return par


async def get_participant_by_idfide(idfide: str) -> ParticipantItem:
    filter = {"_model": ParticipantItem}
    filter["_fieldlist"] = list(filter["_model"].model_fields.keys())
    filter["idfide"] = idfide
    return await DbParticpant.find_single(filter)


async def import_registration(idenr) -> str:
    """
    import an enrollemnt and create a participant
    return the id of the participant
    """
    enr = cast(Registration, await get_registration(idenr))
    return await DbParticpant.add(
        {
            "badgeimage": enr.badgeimage,
            "badgemimetype": enr.badgemimetype,
            "badgelength": enr.badgelength,
            "birthyear": enr.birthyear,
            "category": ParticipantCategory(enr.category.value),
            "chesstitle": enr.chesstitle or "",
            "enabled": True,
            "emails": enr.emailplayer.split(","),
            "first_name": enr.first_name,
            "gender": Gender(enr.gender),
            "idbel": enr.idbel,
            "idclub": enr.idclub,
            "idfide": enr.idfide,
            "locale": enr.locale,
            "last_name": enr.last_name,
            "nationalityfide": enr.nationalityfide,
            "present": None,
            "ratingbel": enr.ratingbel or 0,
            "ratingfide": enr.ratingfide or 0,
            "registrationtime": enr.registrationtime,
            "remarks": "",
        }
    )


async def import_registrations():
    """
    import all enrollment for the bjk 2024
    check doubles
    retain most recent enrollment for the same person
    """
    enrs = await get_registrations({"confirmed": True})
    idfides = {}
    for enr in enrs:
        if enr.idfide in idfides:
            # we have a double detected via idfide
            if enr.registrationtime > idfides[enr.idfide].registrationtime:
                idfides[enr.idfide] = enr
        else:
            idfides[enr.idfide] = enr
    # process the participants
    for idfide, enr in idfides.items():
        try:
            par = await get_participant_by_idfide(idfide)
        except RdNotFound:
            par = None
        if par is None:
            await import_registration(enr.id)


async def update_participant(
    id: str, par: ParticipantUpdate, options: dict = {}
) -> Participant:
    opt = options.copy()
    opt["_model"] = opt.pop("_model", ParticipantDetail)
    upd = par.model_dump(exclude_unset=True)
    return cast(
        Participant,
        await DbParticpant.update(id, upd, opt),
    )


async def update_elo() -> None:
    """
    update the elo of all participants
    """
    prts = await get_participants()
    for pr in prts:
        if not pr.enabled:
            continue
        logger.info(f"updating elo {pr.last_name} {pr.first_name}")
        upd = Participant()
        if pr.idbel and pr.idbel != "0":
            try:
                pl = await lookup_idbel(pr.idbel)
                upd.ratingbel = pl.ratingbel
            except Exception as e:
                logger.info(f"lookup idbel failed {pr.last_name} {pr.first_name}")
        if pr.idfide and pr.idfide != "0":
            try:
                pl = await lookup_idfide(pr.idfide)
                upd.ratingfide = pl.ratingfide
            except Exception as e:
                logger.info(f"lookup idfide failed {pr.last_name} {pr.first_name}")
        if upd:
            await update_participant(pr.id, upd)


async def generate_badges(cat: str, ids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    cat: str
    ids: comma separated ids
    """
    # filter: Dict[str, Any] = {"enabled": True}
    if cat:
        prts = await get_participants({"category": cat})
    else:
        prts = await get_participants({"idbel": {"$in": ids.split(",")}})
    logger.info(f"nr of participants {len(prts)}")
    pages = []
    badges = []
    j = 0
    sorteddocs = sorted(prts, key=lambda x: f"{x.last_name}, {x.first_name}")
    for ix, p in enumerate(sorteddocs):
        rix = j % 2 + 1
        cix = j // 2 + 1
        badge = {
            "first_name": p.first_name,
            "last_name": p.last_name,
            "category": p.category.value,
            # "meals": p.meals or "",
            # "mealsclass": "badge_{}".format(p.meals or "NO"),
            "photourl": f"/api/v1/participant/photo/{p.id}",
            "positionclass": "badge{0}{1}".format(cix, rix),
            "ix": ix,
        }
        # log.info(f"badge: {badge}")
        badges.append(badge)
        j += 1
        if j == 8:
            j = 0
            pages.append(badges)
            badges = []
    if j > 0:
        pages.append(badges)
    tmpl = env.get_template("printbadge.j2")
    return tmpl.render({"pages": pages})


async def generate_namecards(cat: str, ids: str = ""):
    """
    get the Namecards for the bjk by categorie or by ids
    ids: comma separated ids
    """
    if cat:
        prts = await get_participants({"category": cat})
    else:
        prts = await get_participants({"idfide": {"$in": ids.split(",")}})
    logger.info(f"nr of participants {len(prts)}")
    pages = []
    cards = []
    j = 0
    sorteddocs = sorted(prts, key=lambda x: f"{x.last_name}, {x.first_name}")
    for ix, p in enumerate(sorteddocs):
        rix = j % 2 + 1
        ct = ""
        # ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            "fullname": "{0}{1} {2}".format(ct, p.last_name, p.first_name),
            "natrating": p.ratingbel or 0,
            "fiderating": p.ratingfide or 0,
            "category": p.category.value,
            "nationalityfide": p.nationalityfide,
            # 'photourl': '/photo/{0}'.format(p.id),
            "positionclass": "card_1{0}".format(rix),
            "ix": ix,
        }
        cards.append(card)
        j += 1
        if j == 2:
            j = 0
            pages.append(cards)
            cards = []
    if j > 0:
        pages.append(cards)
    tmpl = env.get_template("printnamecard.j2")
    return tmpl.render({"pages": pages})


async def get_photo(id: str) -> Response:
    photo = await DbParticpant.find_single(
        {
            "id": id,
            "_fieldlist": ["badgeimage", "badgemimetype"],
        }
    )
    return Response(content=photo["badgeimage"], media_type=photo["badgemimetype"])


async def upload_photo(id: str, photo: str) -> None:
    try:
        header, data = photo.split(",")
        imagedata = a2b_base64(data)
        su = ParticipantUpdate(
            badgemimetype=header.split(":")[1].split(";")[0],
            badgeimage=imagedata,
            badgelength=len(cast(str, imagedata)),
        )
    except Exception:
        raise RdBadRequest(description="BadPhotoData")
    await update_participant(id, su)


# async def generate_prizes():
#     """
#     get the prizes for the bjk by categorie
#     """
#     from cocoon.paymentrequest.paymentrequest import getPaymessage

#     pages = []
#     cards = []
#     j = 0
#     for cat in ["U8", "U10", "U12", "U14", "U16", "U18", "U20"]:
#         for pr in prizetable[cat]:
#             pls = await get_participants({"idbel": str(pr[0])})
#             pl = pls[0]
#             rix = j % 3 + 1
#             code = 2024 * 100000 + pr[0]
#             card = {
#                 "name": "{0}, {1}".format(pl.last_name, pl.first_name),
#                 "category": cat,
#                 "positionclass": "prize_1{0}".format(rix),
#                 "place": pr[1],
#                 "prize": pr[2],
#                 "code": getPaymessage(code),
#             }
#             cards.append(card)
#             j += 1
#             if j == 3:
#                 j = 0
#                 pages.append(cards)
#                 cards = []
#     if j > 0:
#         pages.append(cards)
#     tmpl = env.get_template("printprize.j2")
#     return tmpl.render({"pages": pages})
