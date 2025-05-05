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
    Convert emails to emailplayer
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
