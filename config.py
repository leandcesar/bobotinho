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


class vars:
    """Variáveis de ambiente."""
    class api:
        coinapi = os.environ.get("APIKEY_COINAPI")
        exchangerate = os.environ.get("APIKEY_EXCHANGERATE")
        # tmdb = os.environ.get("APIKEY_TMDB")
        owm = os.environ.get("APIKEY_OWM")
        
    class bot:
        id = int(os.environ.get("BOT_ID"))
        nick = os.environ.get("BOT_NICK")
        prefix = os.environ.get("PREFIX")
    
    class owner:
        id = int(os.environ.get("OWNER_ID"))
        nick = os.environ.get("OWNER_NICK")
    
    class client:
        id = os.environ.get("CLIENT_ID")
        secret = os.environ.get("CLIENT_SECRET")
        token = os.environ.get("TMI_TOKEN")

    database = os.environ.get("DATABASE_URL")
    