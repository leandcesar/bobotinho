# -*- coding: utf-8 -*-
import os


class Config:
    stage: str = os.environ.get("ENV", "dev")
    version: str = os.environ.get("VERSION", "0.1.0")
    access_token: str = os.environ["ACCESS_TOKEN"]
    client_secret: str = os.environ["CLIENT_SECRET"]
    prefix: str = os.environ.get("PREFIX", "%")
    dev: str = os.environ.get("DEV_NICK")
    color = int(os.environ.get("COLOR", "9147FF"), base=16)
    site_url: str = os.environ.get("SITE_URL")
    bugs_url: str = os.environ.get("DISCORD_WEBHOOK_BUGS")
    suggestions_url: str = os.environ.get("DISCORD_WEBHOOK_SUGGESTIONS")
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")
    log_filename: str = os.environ.get("LOG_FILE_CONFIG", "logging_config.ini")
    database_url: str = os.environ.get("DATABASE_URL", "sqlite://:memory:")
    redis_url: str = os.environ.get("REDIS_URL")
    api_key: str = os.environ.get("BOBOTINHO_API_KEY")
    analytics_key: str = os.environ.get("ANALYTICS_KEY")
    bugsnag_key: str = os.environ.get("BUGSNAG_KEY")
