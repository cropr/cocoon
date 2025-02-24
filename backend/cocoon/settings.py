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
    "bcc_registration": "cocoon@kosk.be,ruben.decrop@gmail.com",
    "account": "ruben@kosk.be",
}


FILESTORE = {
    "manager": "google",
    "bucket": os.environ.get("FILESTORE_BUCKET", "cocoon-kosk.appspot.com"),
}

GOOGLE_CLIENT_ID = (
    "899786740417-dhtk8pilvkhkne3ht3c6ecbnm0619ijm.apps.googleusercontent.com"
)
GOOGLE_LOGIN_DOMAINS = ["kosk.be"]
GOOGLE_PROJECT_ID = "cocoon-kosk"

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
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "cocoon": {
            "handlers": ["console"],
            "level": os.getenv("COCOON_LOGLEVEL", "INFO"),
            "propagate": False,
        },
        "reddevil": {
            "handlers": ["console"],
            "level": os.getenv("REDDEVIL_LOGLEVEL", "INFO"),
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

SECRETS_PATH = Path(os.environ.get("SECRETS_PATH", "./shared/secrets"))

TEMPLATES_PATH = Path(os.environ.get("TEMPLATES_PATH", "./backend/cocoon/templates"))

TOKEN = {
    "timeout": 180,  # timeout in minutes
    "secret": "kennehvrowe,endaklaagtendazaagt",
    "algorithm": "HS256",
    "nocheck": False,
}

ls = "No local settings found"

if COCOON_MODE == "local":
    ls = "importing local settings"
    from env_local import *  # noqa F403


if COCOON_MODE == "prodtest":
    ls = "importing prodtest settings"
    from env_prodtest import *  # noqa F403

if COLORLOG:
    LOG_CONFIG["handlers"]["console"]["formatter"] = "color"  # type: ignore

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)
logger.info(ls)
