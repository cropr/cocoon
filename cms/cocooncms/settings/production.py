# ruff: noqa: F405
import os
import random
import string

from .base import *  # noqa: F403

DEBUG = False

# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
if "DJANGO_SECRET_KEY" in os.environ:
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print(  # noqa: T201
        "WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY."
    )
    SECRET_KEY = "".join(
        [random.SystemRandom().choice(string.printable) for i in range(50)]
    )

# Make sure Django can detect a secure connection properly on Heroku:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Accept all hostnames, since we don't know in advance which hostname will be used for any given Heroku instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# This is used by Wagtail's email notifications for constructing absolute
# URLs. Please set to the domain that users will access the admin site.
if "PRIMARY_HOST" in os.environ:
    WAGTAILADMIN_BASE_URL = "https://{}".format(os.environ["PRIMARY_HOST"])

# AWS creds may be used for S3 and/or Elasticsearch
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "")


# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
STORAGES["staticfiles"]["BACKEND"] = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

if "GS_BUCKET_NAME" in os.environ:
    GS_BUCKET_NAME = os.getenv("GS_BUCKET_NAME")
    GS_PROJECT_ID = os.getenv("GS_PROJECT_ID")
    GS_DEFAULT_ACL = "publicRead"
    GS_AUTO_CREATE_BUCKET = True

    INSTALLED_APPS.append("storages")
    STORAGES["default"]["BACKEND"] = "storages.backends.gcloud.GoogleCloudStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}

# Front-end cache
# This configuration is used to allow purging pages from cache when they are
# published.
# These settings are usually used only on the production sites.
# This is a configuration of the CDN/front-end cache that is used to cache the
# production websites.
# https://docs.wagtail.org/en/stable/reference/contrib/frontendcache.html
# The backend can be configured to use an account-wide API key, or an API token with
# restricted access.
if (
    "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in os.environ
    or "FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN" in os.environ
):
    INSTALLED_APPS.append("wagtail.contrib.frontend_cache")
    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "ZONEID": os.environ["FRONTEND_CACHE_CLOUDFLARE_ZONEID"],
        }
    }

    if "FRONTEND_CACHE_CLOUDFLARE_TOKEN" in os.environ:
        # To use an account-wide API key, set the following:
        #  * $FRONTEND_CACHE_CLOUDFLARE_TOKEN
        #  * $FRONTEND_CACHE_CLOUDFLARE_EMAIL
        #  * $FRONTEND_CACHE_CLOUDFLARE_ZONEID
        # These can be obtained from a sysadmin.
        WAGTAILFRONTENDCACHE["default"].update(
            {
                "EMAIL": os.environ["FRONTEND_CACHE_CLOUDFLARE_EMAIL"],
                "TOKEN": os.environ["FRONTEND_CACHE_CLOUDFLARE_TOKEN"],
            }
        )

    else:
        # To use an API token with restricted access, set the following:
        #  * $FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN
        #  * $FRONTEND_CACHE_CLOUDFLARE_ZONEID
        WAGTAILFRONTENDCACHE["default"].update(
            {"BEARER_TOKEN": os.environ["FRONTEND_CACHE_CLOUDFLARE_BEARER_TOKEN"]}
        )

# Force HTTPS redirect (enabled by default!)
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = True

# This will allow the cache to swallow the fact that the website is behind TLS
# and inform the Django using "X-Forwarded-Proto" HTTP header.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# This is a setting activating the HSTS header. This will enforce the visitors to use
# HTTPS for an amount of time specified in the header. Since we are expecting our apps
# to run via TLS by default, this header is activated by default.
# The header can be deactivated by setting this setting to 0, as it is done in the
# dev and testing settings.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-seconds
DEFAULT_HSTS_SECONDS = 30 * 24 * 60 * 60  # 30 days
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", DEFAULT_HSTS_SECONDS))  # noqa

# Do not use the `includeSubDomains` directive for HSTS. This needs to be prevented
# because the apps are running on client domains (or our own for staging), that are
# being used for other applications as well. We should therefore not impose any
# restrictions on these unrelated applications.
# https://docs.djangoproject.com/en/stable/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True

# https://docs.djangoproject.com/en/stable/ref/settings/#secure-content-type-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# Referrer-policy header settings.
# https://django-referrer-policy.readthedocs.io/en/1.0/

REFERRER_POLICY = os.environ.get(  # noqa
    "SECURE_REFERRER_POLICY", "no-referrer-when-downgrade"
).strip()

# Allow the redirect importer to work in load-balanced / cloud environments.
# https://docs.wagtail.org/en/stable/reference/settings.html#redirects
WAGTAIL_REDIRECTS_FILE_STORAGE = "cache"
