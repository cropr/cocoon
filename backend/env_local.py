from pathlib import Path

COLORLOG = True

EMAIL = {
    "backend": "SMTP",
    "host": "localhost",
    "port": "1025",
    "sender": "noreply@",
    "bcc_reservation": "ruben.decrop@gmail.com,floreal@cocoon.be",
    "bcc_enrollment": "ruben.decrop@gmail.com,luc.cornet@cocoon.be",
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
