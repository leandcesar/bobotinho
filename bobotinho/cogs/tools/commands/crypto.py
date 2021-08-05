# -*- coding: utf-8 -*-
from bobotinho.apis import Crypto
from bobotinho.utils import convert

description = "Saiba o valor da conversão de uma criptomoeda em reais"
aliases = ["bitcoin", "ethereum"]
usage = "digite o comando, a sigla (ex: BTC) e a quantidade para saber a conversão em reais"


async def command(ctx, arg1: str = "", arg2: str = ""):
    translate = {"bitcoin": "BTC", "ethereum": "ETH"}
    target = "BRL"
    invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):]
    base = translate.get(invoke_by) or arg1.upper()
    amount = convert.str2float(arg1) or convert.str2float(arg2) or 1.0
    if base and (conversion := await Crypto.conversion(base, target)):
        try:
            total = conversion / amount
            amount = convert.number2str(amount)
            total = convert.number2str(total)
            ctx.response = f"{amount} {base} = {total} {target}"
        except Exception:
            ctx.response = "a conversão ultrapassou um valor extremamente alto"
    elif base:
        ctx.response = "não encontrei nenhuma moeda com a sigla informada"
