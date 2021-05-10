# -*- coding: utf-8 -*-
import aiohttp
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
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    return await request(url, "get", res_method, raise_for_status, *args, **kwargs)


async def post(
    url: str,
    res_method: str = "json",
    raise_for_status: bool = True,
    *args,
    **kwargs
) -> Optional[Union[str, dict]]:
    return await request(url, "post", res_method, raise_for_status, *args, **kwargs)
