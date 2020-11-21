# -*- coding: utf-8 -*-

import config
import datetime
import googletrans
import re

from ext.command import command
from twitchio.ext import commands
from utils import asyncrq, convert

URL_MATH = "https://api.mathjs.org/v4/?expr={operation}&precision=4"
URL_CURRENCY = "https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
URL_CRYPTO = "https://rest.coinapi.io/v1/exchangerate/{base}/{target}"


def is_float(value: str):
    try:
        float(value.replace(",", "."))
        return True
    except:
        return False


class Tools(commands.AutoCog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = googletrans.Translator()

    def _prepare(self, bot):
        pass

    @command(
        aliases=["bitcoin", "ethereum"], 
        description="saiba o valor da conversão de uma criptomoeda em reais", 
        usage="digite o comando, a sigla da criptomoeda (ex: BTC) e a quantidade (opcional) para saber a conversão em reais"
    )
    async def crypto(self, ctx, code: str = None, amount: str = None):
        if ctx.command.invoked_by != ctx.command.name:
            code = dict(bitcoin="BTC", ethereum="ETH").get(ctx.command.invoked_by)
            if not code or not is_float(code):
                amount = 1.00
            else:
                amount = float(code.replace(",", "."))
        elif not code or (is_float(code) and not amount):
            return
        elif not is_float(code) and not amount:
            amount = 1.0
        elif not is_float(code) and is_float(amount):
            amount = float(amount.replace(",", "."))
        elif is_float(code) and not is_float(amount):
            code, amount = amount, float(code.replace(",", "."))
        
        base = code.upper()
        target = "BRL"
        url = URL_CRYPTO.format(base=base, target=target)
        headers = {'X-CoinAPI-Key': config.Vars.apikey_coinapi}
        try:
            response = await asyncrq.get(url, headers=headers)
            conversion = response["rate"]
        except:
            ctx.response = f"@{ctx.author.name}, a sigla da moeda informada não foi encontrada"
        else:
            total = conversion * amount
            if total > 1e15:
                ctx.response = f"@{ctx.author.name}, a conversão ultrapassou 1 quadrilhão de reais"
            else:
                amount = convert.number(amount)
                total = convert.number(total)
                ctx.response = f"@{ctx.author.name}, {amount} {base} = {total} {target}"

    @command(
        aliases=["dolar", "euro", "libra"], 
        description="saiba o valor da conversão de uma moeda em reais", 
        usage="digite o comando, a sigla da moeda (ex: USD) e a quantidade (opcional) para saber a conversão em reais"
    )
    async def currency(self, ctx, code: str = None, amount: str = None):
        if ctx.command.invoked_by != ctx.command.name:
            if not code or not is_float(code):
                amount = 1.00
            else:
                amount = float(code.replace(",", "."))
            code = dict(dolar="USD", euro="EUR", libra="GBP").get(ctx.command.invoked_by)
        elif not code or (is_float(code) and not amount):
            return
        elif not is_float(code) and not amount:
            amount = 1.0
        elif not is_float(code) and is_float(amount):
            amount = float(amount.replace(",", "."))
        elif is_float(code) and not is_float(amount):
            code, amount = amount, float(code.replace(",", "."))
        
        target = code.upper()
        base = "BRL"
        url = URL_CURRENCY.format(api_key=config.Vars.apikey_exchangerate, base=base)
        try:
            response = await asyncrq.get(url)
            conversion_rates = response["conversion_rates"]
        except Exception as err:
            self.bot.log.error(err)
            ctx.response = f"@{ctx.author.name}, não foi possível verificar isso"
        else:
            if conversion_rates.get(target, None):
                total = amount / conversion_rates[target]
                if total > 1e15:
                    ctx.response = f"@{ctx.author.name}, a conversão ultrapassou 1 quadrilhão de reais"
                else:
                    amount = convert.number(amount)
                    total = convert.number(total)
                    ctx.response = f"@{ctx.author.name}, {amount} {target} = {total} {base}"
            else:
                ctx.response = f"@{ctx.author.name}, a sigla da moeda informada não foi encontrada"

    @command(description="saiba o resultado de alguma expressão matemática", usage="digite o comando e uma expressão matemática para receber o resultado")
    async def math(self, ctx, *, operation: str):
        operation = (
            operation.lower()
            .replace("%", "%25")
            .replace("+", "%2B")
            .replace(" ", "")
            .replace("÷", "/")
            .replace("×", "*")
            .replace("x", "*")
        )
        result = await asyncrq.get(URL_MATH.format(operation=operation), res_method="text")
        result = (
            result.lower()
            .replace("infinity", "infinito")
            .replace("nan", "🤯")
        )
        ctx.response = f"@{ctx.author.name}, {result}"

    @command(description="saiba a tradução de alguma mensagem", usage="digite o comando e um texto para ser traduzido")
    async def translate(self, ctx, langs: str, *, text: str = None):            
        src = "auto"
        dest = "pt"
        if not text:
            text = langs
        else:
            match = re.match(r"(\w{2})?->(\w{2})?", langs)
            if match:
                _src, _dest = match.groups()
                if _src and _src in googletrans.LANGUAGES:
                    src = _src
                if _dest and _dest in googletrans.LANGUAGES:
                    dest = _dest
                if not _src and not _dest:
                    text = langs + " " + text
            else:
                text = langs + " " + text
                    
        try:
            translation = await self.bot.loop.run_in_executor(
                None, self.translator.translate, text, dest, src
            )
        except Exception as err:
            self.bot.log.error(err)
            ctx.response = f"@{ctx.author.name}, não foi possível traduzir isso"
        else:
            ctx.response = f"@{ctx.author.name}, {src}->{dest}: {translation.text}"

        if not translation.text or translation.text == text:
            src = "auto"
            dest = "en" if dest == "pt" else "pt"
            try:
                translation = await self.bot.loop.run_in_executor(
                    None, self.translator.translate, text, dest, src
                )
            except Exception as err:
                self.bot.log.error(err)
                ctx.response = f"@{ctx.author.name}, não foi possível traduzir isso"
            else:
                ctx.response = f"@{ctx.author.name}, {src}->{dest}: {translation.text}"


def prepare(bot):
    bot.add_cog(Tools(bot))


def breakdown(bot):
    pass
