from . import router
from cocoon.participant import get_participants, update_participant, ParticipantUpdate
from cocoon.registration import lookup_idfide


@router.post("/emails", status_code=201)
async def emails2emailplayer():
    """
    Convert emails to emailplayer
    """
    pars = await get_participants()
    for par in pars:
        if par.emails and isinstance(par.emails, list):
            pu = ParticipantUpdate(emailplayer=",".join(par.emails))
            await update_participant(par.id, pu)


@router.post("/elo_update", status_code=201)
async def elo_update():
    """
    update elo
    """
    pars = await get_participants()
    for par in pars:
        p = await lookup_idfide(par.idfide)
        pu = ParticipantUpdate(chesstitle=p.chesstitle, ratingfide=p.ratingfide)
        await update_participant(par.id, pu)


@router.get("/elo_tom")
async def elo_tom():
    tom = await lookup_idfide("201952")
    return tom


@router.get("/badges")
async def generate_badges(category: str = None):
    """
    get the badges for the vl
    """
    prts = await get_attendees_vk(filter)
    logger.info(f"nr of attendees {len(prts)}")
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
            # "rating": max(p.ratingbel or 0, p.ratingfide or 0),
            "chesstitle": "",
            "category": p.category.value,
            # "meals": p.meals or "",
            # "mealsclass": "badge_{}".format(p.meals or "NM"),
            # "photourl": f"/photo/{p.id}",
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
    tmpl = env.get_template("printbadge_vk.j2")
    return tmpl.render({"pages": pages})
