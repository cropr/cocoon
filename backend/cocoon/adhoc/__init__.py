from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/adhoc")

import cocoon.adhoc.participant  # noqa F401
