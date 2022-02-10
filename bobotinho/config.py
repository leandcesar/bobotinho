# -*- coding: utf-8 -*-
import os
import sys


class Config:
    version = os.environ.get("VERSION", "0.1.0")
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    access_token = os.environ.get("ACCESS_TOKEN")
    client_secret = os.environ.get("CLIENT_SECRET")
    prefix = os.environ.get("BOT_PREFIX", "%")
    dev = os.environ.get("DEV_NICK")
    site_url = os.environ.get("BOT_SITE_URL")
    bugs_webhook_url = os.environ.get("DISCORD_WEBHOOK_BUGS")
    suggestions_webhook_url = os.environ.get("DISCORD_WEBHOOK_SUGGESTIONS")
    color_bot = os.environ.get("COLOR_BOT", 0x9147FF)


class ApiConfig:
    analytics_url = os.environ.get("API_ANALYTICS_URL", "https://tracker.dashbot.io/track")
    analytics_key = os.environ.get("API_ANALYTICS_KEY")
    bugsnag_key = os.environ.get("API_BUGSNAG_KEY")
    color_url = os.environ.get("API_COLOR_URL", "https://www.thecolorapi.com")
    currency_key = os.environ.get("API_CURRENCY_KEY")
    dicio_url = os.environ.get("API_DICIO_URL", "http://www.dicio.com.br")
    math_url = os.environ.get("API_MATH_URL", "https://api.mathjs.org/v4")
    twitch_url = os.environ.get("API_TWITCH_URL", "http://decapi.me/twitch")
    weather_key = os.environ.get("API_WEATHER_KEY")


class ProdConfig(Config, ApiConfig):
    mode = "prod"
    database_url = os.environ.get("DATABASE_URL")
    redis_url = os.environ.get("REDIS_URL")


class LocalConfig(Config, ApiConfig):
    mode = "local"
    if os.environ.get("DATABASE_URL"):
        database_url = os.environ["DATABASE_URL"]
    else:
        database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        database_file = os.path.join(database_dir, "db.sqlite3")
        database_url = f"sqlite:///{database_file}"
    redis_url = os.environ.get("REDIS_URL")


class TestConfig(Config, ApiConfig):
    mode = "test"
    database_url = "sqlite://:memory:"
    redis_url = None
    bugsnag_key = None


try:
    config_options = {"prod": ProdConfig, "local": LocalConfig, "test": TestConfig}
    config_mode = os.environ.get("CONFIG_MODE", "local")
    config = config_options[config_mode]
except KeyError:
    sys.exit(f"[CRITICAL] Invalid <CONFIG_MODE>. Expected 'local', 'test' or 'prod', not '{config_mode}'.")
else:
    print(f"[INFO] Running with <CONFIG_MODE>='{config.mode}'")
