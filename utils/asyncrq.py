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

from aiohttp import ClientError
from http import HTTPStatus


async def check_response(response, res_method, status, body):
    """Verifica se a resposta foi obtida com sucesso."""
    if HTTPStatus.OK <= status <= HTTPStatus.IM_USED:
        return await getattr(response, res_method)()
    raise ClientError(f"{status}: {body}")


async def query(url, method="get", res_method="json", *args, **kwargs):
    """Abre uma sessão e executa o método para obter uma resposta."""
    async with aiohttp.ClientSession() as session:
        try:
            async with getattr(session, method)(url, *args, **kwargs) as response:
                check_response(response, res_method, response.status, await response.text())
        except ClientError as e:
            raise ClientError(f"{e.__class__.__name__}: {e}")


async def get(url, *args, **kwargs):
    """Solicita recursos do servidor."""
    return await query(url, "get", *args, **kwargs)


async def post(url, *args, **kwargs):
    """Envia dados para processamento ao servidor."""
    return await query(url, "post", *args, **kwargs)
