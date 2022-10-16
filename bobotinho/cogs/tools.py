# -*- coding: utf-8 -*-
import re

from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, Message, cooldown, command, helper, usage
from bobotinho.services.currency import Currency
from bobotinho.services.math import Math
from bobotinho.services.translator import Translator
from bobotinho.services.weather import Weather
from bobotinho.utils.convert import json_to_dict
from bobotinho.utils.time import timeago

AFKs = json_to_dict("bobotinho//data//afk.json")


class Tools(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot
        self.bot.listeners.insert(1, self.listener_afk)
        self.currency_api = Currency(key=config.currency_key)
        self.math_api = Math()
        self.translator_api = Translator()
        self.weather_api = Weather(key=config.weather_key)

    def cog_unload(self) -> None:
        self.bot.loop.create_task(self.currency_api.close())
        self.bot.loop.create_task(self.math_api.close())
        self.bot.loop.create_task(self.translator_api.close())
        self.bot.loop.create_task(self.weather_api.close())

    async def listener_afk(self, ctx: Context) -> bool:
        if not self.bot.is_enabled(ctx, "afk"):
            return False
        if ctx.command:
            return False
        if not ctx.user or not ctx.user.status or ctx.user.status.online:
            return False
        delta = timeago(ctx.user.status.updated_on).humanize(short=True)
        action = [afk for afk in AFKs if afk["alias"] == ctx.user.status.alias][0]["returned"]
        await ctx.reply(f"você {action}: {ctx.user.status.message} (há {delta})")
        ctx.user.update_status(online=True)
        return True

    @helper("informe que você está se ausentando do chat")
    @cooldown(rate=1, per=30, bucket=Bucket.member)
    @command(aliases=[afk["alias"] for afk in AFKs if afk["alias"] != "afk"])
    async def afk(self, ctx: Context, *, content: str = "") -> None:
        if len(content) >= 450:
            return await ctx.reply("essa mensagem é muito comprida")
        invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
        afk = [afk for afk in AFKs if afk["alias"] == invoke_by][0]
        alias = afk["alias"]
        action = afk["afk"]
        message = content or afk["emoji"]
        ctx.user.update_status(online=False, alias=alias, message=message)
        return await ctx.reply(f"você {action}: {message}")

    @helper("saiba o valor da conversão de uma moeda em reais")
    @usage("digite o comando, a sigla da moeda (ex: USD, BTC) e a quantidade para saber a conversão em reais")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["crypto"])
    async def currency(self, ctx: Context, base: str, amount: int = 1) -> None:
        conversion = await self.currency_api.rate(base=base, quote="BRL")
        total = amount * conversion
        return await ctx.reply(f"{base.upper()} {amount:.2f} = BRL {total:.2f}")

    @helper("saiba o valor da conversão de uma moeda em reais")
    @usage("digite o comando e a quantidade para saber a conversão em reais")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["euro", "libra", "bitcoin", "ethereum"])
    async def dolar(self, ctx: Context, amount: int = 1) -> None:
        invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
        aliases = {"dolar": "USD", "euro": "EUR", "libra": "GBP", "bitcoin": "BTC", "ethereum": "ETH"}
        base = aliases[invoke_by]
        conversion = await self.currency_api.rate(base=base, quote="BRL")
        total = amount * conversion
        return await ctx.reply(f"{base.upper()} {amount:.2f} = BRL {total:.2f}")

    @helper("saiba o resultado de alguma expressão matemática")
    @usage("digite o comando e uma expressão matemática (ex: 1+1)")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["evaluate", "calc"])
    async def math(self, ctx: Context, *, content: str) -> None:
        try:
            result = await self.math_api.evaluate(expression=content)
            return await ctx.reply(result.replace("Infinity", "infinito").replace("NaN", "🤯"))
        except Exception:
            return await ctx.reply(
                "não consegui calcular isso... lembre-se: use * para multiplicação, "
                "use / para divisão, e use ponto em vez de vírgula para números decimais"
            )

    @helper("retome seu status de ausência do chat")
    @usage("digite o comando em até 2 minutos após ter retornado do seu AFK para retomá-lo")
    @cooldown(rate=3, per=60)
    @command(aliases=["r" + afk["alias"] for afk in AFKs if afk["alias"] != "afk"])
    async def rafk(self, ctx: Context) -> None:
        # TODO: %rafk
        raise NotImplementedError()

    @helper("saiba a tradução de alguma mensagem")
    @usage("digite o comando e um texto para ser traduzido")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["t"])
    async def translate(self, ctx: Context, options: str, *, content: str = "") -> None:
        match = re.match(r"(\w{2})?->(\w{2})?", options)  # source->target or source-> or ->target
        if match:
            source, target = match.groups()
        else:
            content = f"{options} {content}"
            source = target = None
        source = source if source else "auto"
        target = target if target else "pt"
        translation = self.translator_api.translate(text=content, source=source, target=target)
        if not translation or translation == content:
            return await ctx.reply("não foi possível traduzir isso")
        return await ctx.reply(translation)

    @helper("saiba o clima atual de alguma cidade")
    @usage("digite o comando e o nome de um local para saber o clima")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["wt"])
    async def weather(self, ctx: Context, *, content: str) -> None:
        if "," not in content:
            content = f"{content}, br"
        try:
            weather = await self.weather_api.prediction(location=content)
            city = weather["name"]
            country = weather["country"]
            status = weather["description"]
            temperature = weather["temp"]
            feels_like = weather["temp_feels_like"]
            wind = weather["speed"]
            humidiy = weather["humidity"]
            emoji = weather["emoji"]
            return await ctx.reply(
                f"em {city} ({country}): {status} {emoji}, {temperature}°C (sensação de "
                f"{feels_like}°C), ventos a {wind}m/s e {humidiy}% de umidade"
            )
        except Exception:
            return await ctx.reply("não há nenhuma previsão para esse local")


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Tools(bot))
