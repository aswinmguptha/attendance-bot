#!/usr/bin/python3
if not __name__.endswith("sample_config"):
    import sys
    print(
        "The README is there to be read."
        "Extend this sample config to a config file, "
        "don't just rename and change "
        "values here. "
        "Doing that WILL backfire on you.\n"
        "Bot quitting.",
        file=sys.stderr
    )
    quit(1)


# Create a new config.py file in same dir and import, then extend this class.
import os


class Config:
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", None)
    USE_WEBHOOKS = bool(os.environ.get("USE_WEBHOOKS", False))
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", None)
    PORT = int(os.environ.get("PORT", 5000))
    DATABASE_URL = os.environ.get("DATABASE_URL", None)


class Development(Config):
    pass
