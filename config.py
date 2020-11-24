# -*- coding: utf-8 -*-

"""
bobotinho - Twitch bot for Brazilian offstream chat entertainment
Copyright (C) 2020  Leandro César

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
    