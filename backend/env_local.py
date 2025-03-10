from pathlib import Path

COLORLOG = True

EMAIL = {
    "backend": "SMTP",
    "host": "maildev.decrop.net",
    "port": "1025",
    "sender": "noreply@",
    "bcc_registration": "ruben.decrop@gmail.com",
}

FILESTORE = {
    "manager": "file",
    "path": Path(__file__).parent.parent / "shared" / "cloud",
}

SECRETS = {
    "mongodb": {
        "name": "cocoon-mongodb-dev",
        "manager": "filejson",
    },
    "gmail": {
        "name": "cocoon-gmail-prod",
        "manager": "filejson",
    },
    "statamic": {
        "name": "statamic-server",
        "manager": "filejson",
    },
    "known-hosts": {
        "name": "known-hosts",
        "manager": "filejson",
    },
}
