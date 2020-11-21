# -*- coding: utf-8 -*-

import os


class Vars:
    apikey_coinapi = os.environ.get("APIKEY_COINAPI")
    apikey_exchangerate = os.environ.get("APIKEY_EXCHANGERATE")
    # apikey_tmdb = os.environ.get("APIKEY_TMDB")
    apikey_owm = os.environ.get("APIKEY_OWM")
    
    bot_id = int(os.environ.get("BOT_ID"))
    bot_nick = os.environ.get("BOT_NICK")
    owner_id = int(os.environ.get("OWNER_ID"))
    owner_nick = os.environ.get("OWNER_NICK")
    
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    prefix = os.environ.get("PREFIX")
    tmi_token = os.environ.get("TMI_TOKEN")

    database = os.environ.get("DATABASE_URL")
    