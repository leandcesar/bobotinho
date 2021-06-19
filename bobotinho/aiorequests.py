# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import html
from typing import Optional, Union

from bobotinho.logger import log


async def request(
    url: str,
    method: str = "get",
    res_method: str = "json",
    raise_for_status: bool = True,
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    try:
        async with aiohttp.ClientSession(raise_for_status=raise_for_status) as session:
            async with session.request(method, url, *args, **kwargs) as response:
                if res_method == "html":
                    res_text = await getattr(response, "text")()
                    return html.unescape(res_text)
                return await getattr(response, res_method)()
    except Exception as e:
        log.exception(e)


async def get(
    url: str,
    res_method: str = "json",
    raise_for_status: bool = True,
    wait_response: bool = True,
    loop=None,
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    if wait_response:
        return await request(url, "get", res_method, raise_for_status, *args, **kwargs)
    else:
        loop = loop or asyncio.get_event_loop()
        func = request(url, "get", res_method, raise_for_status, *args, **kwargs)
        coro = asyncio.wait_for(func, 30)
        loop.create_task(coro)


async def post(
    url: str,
    res_method: str = "json",
    raise_for_status: bool = True,
    wait_response: bool = True,
    loop=None,
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    if wait_response:
        return await request(url, "post", res_method, raise_for_status, *args, **kwargs)
    else:
        loop = loop or asyncio.get_event_loop()
        func = request(url, "post", res_method, raise_for_status, *args, **kwargs)
        coro = asyncio.wait_for(func, 30)
        loop.create_task(coro)
