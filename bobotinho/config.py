# -*- coding: utf-8 -*-
import os


class Config:
    version = os.environ.get("VERSION", "0.1.0")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    log_filename = os.environ.get("LOG_FILE_CONFIG", "logging_config.ini")
    access_token = os.environ.get("ACCESS_TOKEN")
    client_secret = os.environ.get("CLIENT_SECRET")
    prefix = os.environ.get("BOT_PREFIX", "%")
    dev = os.environ.get("DEV_NICK")
    site_url = os.environ.get("BOT_SITE_URL")
    bugs_url = os.environ.get("DISCORD_WEBHOOK_BUGS")
    suggestions_url = os.environ.get("DISCORD_WEBHOOK_SUGGESTIONS")
    bot_color = os.environ.get("COLOR_BOT", 0x9147FF)
    database_url = os.environ.get("DATABASE_URL", "sqlite://:memory:")
    redis_url = os.environ.get("REDIS_URL")
    api_key = os.environ.get("BOBOTINHO_API_KEY")
    analytics_key = os.environ.get("ANALYTICS_KEY")
    bugsnag_key = os.environ.get("BUGSNAG_KEY")
