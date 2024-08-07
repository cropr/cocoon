# Copyright 2022-2024 Chessdevil Consulting
# Copyright 2015-2024 Ruben Decrop

import os
import logging
from pathlib import Path

COCOON_MODE = os.environ.get("COCOON_MODE", "prod")


COLORLOG = False

EMAIL = {
    "backend": os.environ.get("EMAIL_BACKEND", "GMAIL"),
    "sender": "noreply@kosk.be",
    "bcc_registration": "bestuur@kosk.be",
    "account": "ruben@kosk.be",
}


FILESTORE = {
    "manager": "google",
    "bucket": os.environ.get("FILESTORE_BUCKET", "cocoon-website.appspot.com"),
}

GOOGLE_CLIENT_ID = (
    "464711449307-7j2oecn3mkfs1eh3o7b5gh8np3ebhrdp.apps.googleusercontent.com"
)
GOOGLE_LOGIN_DOMAINS = ["kosk.be"]
GOOGLE_PROJECT_ID = "cocoon-website"

JWT_ALGORITHM = "HS256"
JWT_SECRET = "levedetorrevanostende"

KBSB_HOST = "https://www.frbe-kbsb-ksb.be"

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(levelname)s: %(asctime)s %(name)s %(message)s",
        },
        "color": {
            "format": "%(log_color)s%(levelname)s%(reset)s: %(asctime)s %(bold)s%(name)s%(reset)s %(message)s",
            "()": "reddevil.core.colorlogfactory.c_factory",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "cocoon": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "reddevil": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "fastapi": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

SECRETS = {
    "mongodb": {
        "name": "cocoon-mongodb-prod",
        "manager": "googlejson",
    },
    "gmail": {
        "name": "cocoon-gmail",
        "manager": "googlejson",
    },
    "filestore": {
        "name": "cocoon-filestore",
        "manager": "googlejson",
    },
    "statamic": {
        "name": "statamic-server",
        "manager": "googlejson",
    },
    "known-hosts": {
        "name": "known-hosts",
        "manager": "googlejson",
    },
}

SECRETS_PATH = Path(os.environ.get("SECRETS_PATH", "../shared/secrets"))

TEMPLATES_PATH = Path(os.environ.get("TEMPLATES_PATH", "./cocoon/templates"))

TOKEN = {
    "timeout": 180,  # timeout in minutes
    "secret": "kennehvrowe,endaklaagtendazaagt",
    "algorithm": "HS256",
    "nocheck": False,
}

ls = "No local settings found"

if COCOON_MODE == "local":
    ls = "importing local settings"
    from env_local import *


if COCOON_MODE == "prodtest":
    ls = "importing prodtest settings"
    from env_prodtest import *

if COLORLOG:
    LOG_CONFIG["handlers"]["console"]["formatter"] = "color"  # type: ignore

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
logger.info(ls)
