COLORLOG = True

EMAIL = {
    "backend": "SMTP",
    "host": "maildev.decrop.net",
    "port": "1025",
    "bcc_registration": "cocoon@kosk.be,ruben.decrop@gmail.com",
    "sender": "noreply@kosk.be",
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
