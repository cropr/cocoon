from . import router
from cocoon.participant import get_participants, update_participant, ParticipantUpdate


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
