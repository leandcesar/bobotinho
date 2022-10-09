# -*- coding: utf-8 -*-
from datetime import datetime

from bobotinho import config
from bobotinho.bot import Bobotinho
from bobotinho.ext.commands import Bucket, Cog, Context, Message, cooldown, command, helper, routine, usage
from bobotinho.services.wit_ai import WitAI
from bobotinho.utils.time import timeago
from bobotinho.ext.redis import redis


class Reminder(Cog):
    def __init__(self, bot: Bobotinho) -> None:
        self.bot = bot
        self.bot.listeners.insert(2, self.listener_remind)
        self.routine_remind.start()
        self.witai_api = WitAI(key_duration=config.witai_duration_key, key_datetime=config.witai_datetime_key)

    def cog_unload(self) -> None:
        self.routine_remind.cancel()
        self.bot.loop.create_task(self.witai_api.close())

    async def listener_remind(self, ctx: Context) -> bool:
        if not self.bot.is_enabled(ctx, "remind"):
            return False
        if ctx.command:
            return False
        if not ctx.user or not ctx.user.reminders:
            return False
        if not ctx.user.settings and not ctx.user.settings.mention:
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

    @helper("deixe um lembrete para algum usuário")
    @usage("digite o comando, o nome de alguém e uma mensagem para deixar um lembrete")
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
            text, date = await self.witai_api.get_duration(message=content)
            if text and date:
                content = content.lstrip("in ").replace(text, "").replace(":|:", "")
                delta = timeago(date, reverse=True).humanize(precision=3)
                redis.zadd("reminders", {f"{user.id}:|:{ctx.author.id}:|:{content}:|:{date.isoformat()}:|:{datetime.utcnow().isoformat()}": date.timestamp()})
                return await ctx.reply(f"{mention} será lembrado disso daqui {delta} ⏲️")
            elif text and not date:
                return await ctx.reply("o tempo mínimo para lembretes cronometrados é 1 minuto")

        if content.startswith(("on ", "at ")):
            text, date = await self.witai_api.get_datetime(message=content)
            if text and date:
                content = content.lstrip("at ").lstrip("on ").replace(text, "").replace(":|:", "")
                redis.zadd("reminders", {f"{user.id}:|:{ctx.author.id}:|:{content}:|:{date.isoformat()}:|:{datetime.utcnow().isoformat()}": date.timestamp()})
                date = date.strftime("%d/%m/%Y, às %H:%M:%S")
                return await ctx.reply(f"{mention} será lembrado disso em {date} 📅")
            elif text and not date:
                return await ctx.reply("o tempo mínimo para lembretes agendados é 1 minuto")

        if user.reminders and len(user.reminders) > 15:
            return await ctx.reply(f"já existem muitos lembretes pendentes para {mention}")
        user.add_reminder(user_id=ctx.author.id, message=content)
        return await ctx.reply(f"{mention} será lembrado disso na próxima vez que falar no chat 📝")

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
    bot.add_cog(Reminder(bot))
