# -*- coding: utf-8 -*-
import os


class Config:
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    irc_token = os.getenv("TMI_TOKEN")
    nick = os.getenv("BOT_NAME")
    prefix = os.getenv("BOT_PREFIX")
    site = os.getenv("BOT_SITE")
    ai = bool(os.getenv("BOT_AI_URL"))
    owner = os.getenv("OWNER_NAME")


class ProdConfig(Config):
    database_url = os.getenv("DATABASE_URL")
    redis_url = os.getenv("REDIS_URL")


class LocalConfig(Config):
    __basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    __dbfile = os.path.join(__basedir, "db.sqlite3")
    database_url = f"sqlite:///{__dbfile}"
    redis_url = os.getenv("REDIS_URL")


class TestConfig(Config):
    client_id = None
    client_secret = None
    irc_token = None
    ai = False
    database_url = "sqlite://:memory:"
    redis_url = None


config_dict = {"prod": ProdConfig, "local": LocalConfig, "test": TestConfig}
