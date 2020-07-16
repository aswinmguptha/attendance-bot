#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import importlib
from attendance_bot import (
    updater,
    LOGGER,
    TG_BOT_TOKEN,
    USE_WEBHOOKS,
    WEBHOOK_PORT,
    WEBHOOK_URL
)
from attendance_bot.modules import ALL_MODULES


IMPORTED = {}
for module_name in ALL_MODULES:
    imported_module = importlib.import_module(
        "attendance_bot.modules." + module_name
    )
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception(
            "Can't have two modules with the same name! Please change one"
        )
LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))


if USE_WEBHOOKS:
    LOGGER.info("Using webhooks.")
    updater.start_webhook(
        listen="0.0.0.0",
        port=WEBHOOK_PORT,
        url_path=TG_BOT_TOKEN
    )
    # https://t.me/c/1186975633/22915
    updater.bot.set_webhook(url=WEBHOOK_URL + TG_BOT_TOKEN)
else:
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4)

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()
