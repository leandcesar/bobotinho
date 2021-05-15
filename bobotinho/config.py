# -*- coding: utf-8 -*-
import os


class Config:
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    irc_token = os.getenv("TMI_TOKEN")
    nick = os.getenv("BOT_NAME", "bobotinho")
    prefix = os.getenv("BOT_PREFIX", "%")
    site = os.getenv("BOT_SITE", "https://bobotinho.herokuapp.com")
    owner = os.getenv("OWNER_NAME", "discretinho")


class ProdConfig(Config):
    dbs_url = {
        "db_1": os.getenv("HEROKU_POSTGRESQL_SILVER"),
        "db_2": os.getenv("HEROKU_POSTGRESQL_COPPER"),
        "db_3": os.getenv("HEROKU_POSTGRESQL_RED"),
        "db_4": os.getenv("HEROKU_POSTGRESQL_BLUE"),
    }


class LocalConfig(Config):
    __basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    __dbfile = os.path.join(__basedir, "db.sqlite3")
    dbs_url = {
        "db_1": f"sqlite:///{__dbfile}",
        "db_2": f"sqlite:///{__dbfile}",
        "db_3": f"sqlite:///{__dbfile}",
        "db_4": f"sqlite:///{__dbfile}",
    }


class TestConfig(Config):
    dbs_url = {
        "db_1": "sqlite:///:memory:",
        "db_2": "sqlite:///:memory:",
        "db_3": "sqlite:///:memory:",
        "db_4": "sqlite:///:memory:",
    }


config_dict = {"prod": ProdConfig, "local": LocalConfig, "test": TestConfig}
