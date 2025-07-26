# copyright Ruben Decrop 2012 - 2024
# copyright Chessdevil Consulting 2015 - 2024

import logging
import logging.config

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from reddevil.core import (
    register_app,
    get_settings,
    connect_mongodb,
    close_mongodb,
)

# to support yaml/json mimetype
# import mimetypes

from . import version


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_mongodb()
    yield
    close_mongodb()


# load and register app
app = FastAPI(
    title="Coccon backend",
    description="backend website cocoon.kosk.be",
    version=version,
    lifespan=lifespan,
)
load_dotenv()
register_app(app, "cocoon.settings", "/api")
settings = get_settings()
logger = logging.getLogger(__name__)
# logger.debug("test debug message")
# logger.warning("test warning message")
# logger.info("test info message")
# logger.error("test error message")
# logger.critical("test critical message")
logger.info(f"Starting website cocoon {version} ...")
logger.info(f"Email settings {settings.EMAIL}")

# add CORS middleware for dev only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# import api endpoints
logger.info("loading api_account")
from reddevil.account import api_account  # noqa F401

logger.info("loading api_attendee")
from cocoon.attendee import api_attendee  # noqa F401

logger.info("loading api_filestore")
from reddevil.filestore import api_filestore  # noqa F401

logger.info("loading api_enrollment")
from cocoon.registration import api_registration  # noqa F401

logger.info("loading api_page")
from cocoon.page import api_page  # noqa F401

logger.info("loading api_participant")
from cocoon.participant import api_participant  # noqa F401

logger.info("loading api_paymentrequest")
from cocoon.paymentrequest import api_paymentrequest  # noqa F401

logger.info("loading api_statamic")
from cocoon.statamic import api_statamic  # noqa F401

logger.info("loading api_tournament")
from cocoon.tournament import api_tournament  # noqa F401

app.include_router(api_account.router)
app.include_router(api_attendee.router)
app.include_router(api_registration.router)
app.include_router(api_filestore.router)
app.include_router(api_participant.router)
app.include_router(api_paymentrequest.router)
app.include_router(api_statamic.router)
app.include_router(api_page.router)
app.include_router(api_tournament.router)
logger.info("Api's loaded")

# static files
# app.mount("/css", StaticFiles(directory="../static/css"), name="css")
# app.mount("/img", StaticFiles(directory="../static/img"), name="img")

# fetch the common

#    Simplify operation IDs so that generated API clients have simpler function
#    names.
for route in app.routes:
    if isinstance(route, APIRoute):
        route.operation_id = route.name[4:]

# importing test endpoints
import cocoon.tst_endpoints  # noqa F401

if settings.COCOON_MODE == "prodtest":
    from cocoon.adhoc import router  # noqa F401

    app.include_router(router)
    logger.info("adhoc commands loaded")
