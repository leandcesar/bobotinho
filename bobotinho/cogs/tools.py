# -*- coding: utf-8 -*-
import re

from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, Message, cooldown, command, helper, routine, usage
from bobotinho.ext.redis import redis
from bobotinho.services.currency import Currency
from bobotinho.services.math import Math
from bobotinho.services.translator import Translator
from bobotinho.services.weather import Weather
from bobotinho.services.wit_ai import WitAI
from bobotinho.utils.convert import json_to_dict
from bobotinho.utils.time import datetime, timeago, timedelta

AFKs = json_to_dict("bobotinho//data//afk.json")


class Tools(Cog):
    """Utilitários

    Comandos úteis com ferramentas para facilitar e agilizar sua vida
    """

    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot
        self.bot.listeners.insert(1, self.listener_afk)
        self.bot.listeners.insert(2, self.listener_remind)
        self.currency_api = Currency(key=config.currency_key)
        self.math_api = Math()
        self.translator_api = Translator()
        self.weather_api = Weather(key=config.weather_key)
        self.witai_api = WitAI(key_duration=config.witai_duration_key, key_datetime=config.witai_datetime_key)
        self.routine_remind.start()

    def cog_unload(self) -> None:
        self.bot.loop.create_task(self.currency_api.close())
        self.bot.loop.create_task(self.math_api.close())
        self.bot.loop.create_task(self.translator_api.close())
        self.bot.loop.create_task(self.weather_api.close())
        self.bot.loop.create_task(self.witai_api.close())
        self.routine_remind.cancel()

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

    async def listener_remind(self, ctx: Context) -> bool:
        if not self.bot.is_enabled(ctx, "remind"):
            return False
        if ctx.command:
            return False
        if not ctx.user or not ctx.user.reminders:
            return False
        if ctx.user.settings and not ctx.user.settings.mention:
            return False
        remind = ctx.user.reminders[0]
        if ctx.author.id == remind.user_id:
            twitch_user = ctx.author
        else:
            twitch_user = await self.bot.fetch_user(id=remind.user_id)
        mention = "você" if twitch_user.id == ctx.author.id else f"@{twitch_user.name}"
        content = remind.message or ""
        delta = timeago(remind.created_on).humanize(short=True)
        ctx.response = await ctx.reply(f"{mention} deixou um lembrete: {content} (há {delta})")
        ctx.user.remove_reminder()
        return True

    @helper("informe que você está se ausentando do chat")
    @usage("para usar: %afk <mensagem>")
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
    @usage("para usar: %currency <sigla_da_moeda> <quantidade>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["crypto"])
    async def currency(self, ctx: Context, base: str, amount: int = 1) -> None:
        conversion = await self.currency_api.rate(base=base, quote="BRL")
        total = amount * conversion
        return await ctx.reply(f"{base.upper()} {amount:.2f} = BRL {total:.2f}")

    @helper("saiba o valor da conversão de uma moeda em reais")
    @usage("para usar: %dolar <quantidade>")
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
    @usage("para usar: %math <expressao_matematica>")
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

    @helper("digite o comando em até 2 minutos após ter retornado do seu AFK para retomá-lo")
    @cooldown(rate=3, per=60)
    @command(aliases=["r" + afk["alias"] for afk in AFKs if afk["alias"] != "afk"])
    async def rafk(self, ctx: Context) -> None:
        # TODO: %rafk
        raise NotImplementedError()

    @helper("deixe um lembrete para algum usuário")
    @usage("para usar: %remind <nome_do_usuario> <mensagem>")
    @cooldown(rate=3, per=10, bucket=Bucket.member)
    @command(aliases=["remindme"])
    async def remind(self, ctx: Context, name: str = "", *, content: str = "") -> None:
        invoke_by = ctx.message.content.partition(" ")[0][len(ctx.prefix):].lower()
        if invoke_by == "remindme":
            content = f"{name} {content}"
            name = ctx.author.name
        elif name == "me":
            name = ctx.author.name
        else:
            name = name.lstrip("@").rstrip(",").lower()

        if len(content) > 425:
            return await ctx.reply("essa mensagem é muito comprida")
        elif name == self.bot.nick:
            return await ctx.reply("estou sempre aqui... não precisa me deixar lembretes")
        elif name == ctx.author.name:
            user = ctx.user
        else:
            user = await self.bot.fetch_user_db(name)
            if not user:
                return await ctx.reply(f"@{name} ainda não foi registrado (não usou nenhum comando)")
        if user.settings and not user.settings.mention:
            return await ctx.reply("esse usuário optou por não permitir ser mencionado")

        mention = "você" if name == ctx.author.name else f"@{name}"

        if content.startswith("in "):
            text, seconds = await self.witai_api.get_duration(message=content)
            if not text or not seconds:
                return await ctx.reply(f"não entendi para daqui quanto tempo eu devo te lembrar (ex: {ctx.prefix}remind me in 2min teste)")
            date = datetime.utcnow() + timedelta(seconds=seconds)
            if date and date <= datetime.utcnow() + timedelta(seconds=60):
                return await ctx.reply("o tempo mínimo para lembretes cronometrados é 1 minuto")
            if text and date:
                content = content.lstrip("in ").replace(text, "").replace(":|:", "")
                delta = timeago(date, reverse=True).humanize(precision=3)
                redis.zadd("reminders", {f"{user.id}:|:{ctx.author.id}:|:{content}:|:{date.isoformat()}:|:{datetime.utcnow().isoformat()}": date.timestamp()})
                return await ctx.reply(f"{mention} será lembrado disso daqui {delta} ⏲️")

        if content.startswith(("on ", "at ")):
            text, date_string = await self.witai_api.get_datetime(message=content)
            if date and date <= datetime.utcnow() + timedelta(seconds=60):
                return await ctx.reply("o tempo mínimo para lembretes agendados é 1 minuto")
            date = datetime.fromisoformat(date_string).replace(tzinfo=None)
            if text and date:
                content = content.lstrip("at ").lstrip("on ").replace(text, "").replace(":|:", "")
                redis.zadd("reminders", {f"{user.id}:|:{ctx.author.id}:|:{content}:|:{date.isoformat()}:|:{datetime.utcnow().isoformat()}": date.timestamp()})
                date = date.strftime("%d/%m/%Y, às %H:%M:%S")
                return await ctx.reply(f"{mention} será lembrado disso em {date} 📅")

        if user.reminders and len(user.reminders) > 15:
            return await ctx.reply(f"já existem muitos lembretes pendentes para {mention}")
        user.add_reminder(user_id=ctx.author.id, message=content)
        return await ctx.reply(f"{mention} será lembrado disso na próxima vez que falar no chat 📝")

    @helper("saiba a tradução de alguma mensagem")
    @usage("para usar: %t <mensagem>")
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
    @usage("para usar: %wt <cidade>")
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

    @routine(seconds=30, wait_first=True)
    async def routine_remind(self) -> None:
        now = datetime.utcnow()
        for remind in redis.zrange("reminders", 0, -1):
            user_id_to, user_id_from, content, date_string_to, date_string_from = remind.split(":|:")
            date = datetime.fromisoformat(date_string_to)
            if date > now:
                return None
            if (date - now).total_seconds() >= 3600:
                redis.zrem("reminders", remind)
                continue
            user_to = await self.bot.fetch_user_db(id=user_id_to)
            if user_to.settings and not user_to.settings.mention:
                redis.zrem("reminders", remind)
                continue
            if not self.bot.channels.get(user_to.last_channel) or self.bot.channels[user_to.last_channel].offline:
                continue
            user_from = await self.bot.fetch_user_db(id=user_id_from)
            mention = "você" if user_to.id == user_from.id else f"@{user_to.name}"
            date = datetime.fromisoformat(date_string_from)
            delta = timeago(date).humanize(precision=3, short=True)
            channel = self.bot.get_channel(user_to.last_channel)
            if not channel:
                continue
            await channel.send(f"@{user_to.name}, {mention} deixou um lembrete: {content} (há {delta})")
            redis.zrem("reminders", remind)


def prepare(bot: Bobotinho) -> None:
    bot.add_cog(Tools(bot))
