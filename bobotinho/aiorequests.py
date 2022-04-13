# -*- coding: utf-8 -*-
from aiohttp import ClientResponse, ClientSession
from asyncio import BaseEventLoop, get_event_loop, wait_for
from typing import Optional


async def request(url: str, method: str = "get", raise_for_status: bool = True, *args, **kwargs) -> ClientResponse:
    async with ClientSession(raise_for_status=raise_for_status) as session:
        async with session.request(method, url, *args, **kwargs) as response:
            return response


def no_wait_request(url: str, method: str = "get", raise_for_status: bool = True, loop: BaseEventLoop = None, *args, **kwargs) -> None:
    loop = loop or get_event_loop()
    func = request(url, method, raise_for_status, *args, **kwargs)
    coro = wait_for(func, 10)
    loop.create_task(coro)


async def get(url: str, raise_for_status: bool = True, wait_response: bool = True, loop: BaseEventLoop = None, *args, **kwargs) -> Optional[ClientResponse]:
    if wait_response:
        return await request(url, "get", raise_for_status, *args, **kwargs)
    no_wait_request(url, "get", raise_for_status, loop, *args, **kwargs)


async def post(url: str, raise_for_status: bool = True, wait_response: bool = True, loop: BaseEventLoop = None, *args, **kwargs) -> Optional[ClientResponse]:
    if wait_response:
        return await request(url, "post", raise_for_status, *args, **kwargs)
    no_wait_request(url, "post", raise_for_status, loop, *args, **kwargs)
