#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import os
import i18n
import pathlib
from telegram.ext import Updater


if os.path.exists("attendance_bot/config.py"):
    from attendance_bot.config import Development as Config
else:
    from attendance_bot.sample_config import Development as Config


# LOGGing configurations
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

TG_BOT_TOKEN = Config.TG_BOT_TOKEN
USE_WEBHOOKS = Config.USE_WEBHOOKS
WEBHOOK_URL = Config.WEBHOOK_URL
WEBHOOK_PORT = Config.PORT
DATABASE_URL = Config.DATABASE_URL


# Create the Updater and pass it your bot's token.
# Make sure to set use_context=True to use the new context based callbacks
# Post version 12 this will no longer be necessary
updater = Updater(token=TG_BOT_TOKEN, use_context=True)
# Get the dispatcher to register handlers
dispatcher = updater.dispatcher


BOT_USERNAME = updater.bot.username


i18n.load_path.append(os.path.join((pathlib.Path(__file__).parent).parent, "locale"))
i18n.set("filename_format", "{locale}.{format}")
i18n.set("skip_locale_root_data", True)
i18n.set("fallback", "en")
