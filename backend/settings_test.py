from backend.settings import *  # noqa: F403,F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "card_db.sqlite3",
    }
}

LOGGING = None
