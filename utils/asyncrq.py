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

import aiohttp


async def fetch(url, method="get", res_method="json", *args, **kwargs):
    """Executa uma requisição.
    
    Argumentos:
    url -- endereço HTTP
    method -- método de requisição HTTP
    res_method -- tipo de resposta
    """
    async with aiohttp.ClientSession() as session:
        async with getattr(session, method.lower())(url, *args, **kwargs) as response:
            if response.status == 200:
                return await getattr(response, res_method)()


async def get(url, *args, **kwargs):
    """Executa um GET (compressão sintática para o método GET).
    
    Argumentos:
    url -- endereço HTTP
    """
    return await fetch(url, "get", *args, **kwargs)


async def post(url, *args, **kwargs):
    """Executa um POST (compressão sintática para o método POST).
    
    Argumentos:
    url -- endereço HTTP
    """
    return await fetch(url, "post", *args, **kwargs)
