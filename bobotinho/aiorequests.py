# -*- coding: utf-8 -*-
import aiohttp
import asyncio
from typing import Optional, Union


async def request(
    url: str,
    method: str = "get",
    res_method: str = "json",
    raise_for_status: bool = True,
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    async with aiohttp.ClientSession(raise_for_status=raise_for_status) as session:
        async with session.request(method, url, *args, **kwargs) as response:
            return await getattr(response, res_method)()


def no_wait_request(
    url: str,
    method: str = "get",
    res_method: str = "json",
    raise_for_status: bool = True,
    loop: asyncio.BaseEventLoop = None,
    *args,
    **kwargs
) -> None:
    loop = loop or asyncio.get_event_loop()
    func = request(url, method, res_method, raise_for_status, *args, **kwargs)
    coro = asyncio.wait_for(func, 10)
    loop.create_task(coro)


async def get(
    url: str,
    res_method: str = "json",
    raise_for_status: bool = True,
    wait_response: bool = True,
    loop: asyncio.BaseEventLoop = None,
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    if wait_response:
        return await request(url, "get", res_method, raise_for_status, *args, **kwargs)
    no_wait_request(url, "get", res_method, raise_for_status, loop, *args, **kwargs)


async def post(
    url: str,
    res_method: str = "json",
    raise_for_status: bool = True,
    wait_response: bool = True,
    loop: asyncio.BaseEventLoop = None,
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    if wait_response:
        return await request(url, "post", res_method, raise_for_status, *args, **kwargs)
    no_wait_request(url, "post", res_method, raise_for_status, loop, *args, **kwargs)
