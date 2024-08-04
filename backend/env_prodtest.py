COLORLOG = True

EMAIL = {
    "backend": "SMTP",
    "host": "maildev.decrop.net",
    "port": "1025",
    "sender": "noreply@cocoon.be",
    "bcc_reservation": "ruben.decrop@gmail.com,floreal@cocoon.be",
    "bcc_enrollment": "ruben.decrop@gmail.com,luc.cornet@cocoon.be",
}

SECRETS = {
    "mongodb": {
        "name": "cocoon-mongodb-prod",
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
