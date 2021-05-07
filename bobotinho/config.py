# -*- coding: utf-8 -*-
import os


class Config:
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    irc_token = os.getenv("TMI_TOKEN")
    nick = os.getenv("BOT_NAME", "bobotinho")
    prefix = os.getenv("BOT_PREFIX", "%")
    owner = os.getenv("OWNER_NAME", "discretinho")
    site = os.getenv("URL_SITE", "https://bobotinho.herokuapp.com")
    webhook = os.getenv("URL_LOAD_BALANCER")


class ProdConfig(Config):
    database_url = os.getenv("DATABASE_URL")


class LocalConfig(Config):
    __basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    __dbfile = os.path.join(__basedir, "db.sqlite3")
    database_url = f"sqlite:///{__dbfile}"


class TestConfig(Config):
    database_url = "sqlite:///:memory:"


config_dict = {"prod": ProdConfig, "local": LocalConfig, "test": TestConfig}
