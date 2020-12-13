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

import config
import inspect
import logging
import os

from cogs import afk, remind
from ext import command, channels, postgresql
from twitchio.ext import commands
from utils import checks, convert

logging.basicConfig(
    level=logging.ERROR,
    format='[%(levelname)s] "%(module)s.py", line %(lineno)s, in %(funcName)s: %(message)s',
)


class Bobotinho(commands.Bot):
    def __init__(self):
        """Estabelece comunicação do Bot com a Twitch (IRC)."""
        self.log = logging.getLogger()
        super().__init__(
            irc_token=config.Vars.tmi_token,
            client_id=config.Vars.client_id,
            client_secret=config.Vars.client_secret,
            prefix=config.Vars.prefix,
            nick=config.Vars.bot_nick,
            initial_channels=[config.Vars.bot_nick],
        )

    async def event_error(self, err, data=None):
        """Evento chamado quando ocorre um erro durante o processamento de dados."""
        self.log.error(convert.traceback(err))

    async def event_command_error(self, ctx, err):
        """Evento chamado quando ocorre um erro durante a invocação do comando."""
        if isinstance(err, commands.CheckFailure) and str(err).split()[-1] == "is_enabled":
            # se o comando estiver desativado no canal, envia mensagem alertando
            await ctx.send(f"@{ctx.author.name}, {ctx.prefix}{ctx.command.name} está desativado nesse canal")
        elif isinstance(err, (commands.CommandNotFound, commands.CheckFailure, commands.MissingRequiredArgument)):
            # se o comando não existir,
            # se o usuário não passar em alguma verificação do comando,
            # ou se não fornecer um argumento necessário para o comando
            pass
        else:
            # erro inesperado
            self.log.error(convert.traceback(err))

    async def join_all_channels(self):
        """Método para se juntar à todos os canais do banco de dados."""
        all_channels = await self.db.select_all("channels") # obtém canais e informações
        self.channels = channels.Channels(all_channels) # faz as conversões necessárias
        for i in range(0, len(list(self.channels)), 99):
            # junta-se a cada 99 canais devido a limitação da Twitch
            await self.join_channels(list(self.channels)[i:i+99])

    def load_all_modules(self, path: str = "cogs"):
        """Método que carrega todos os módulos contidos na pasta 'cogs'."""
        for module in [filename[:-3] for filename in os.listdir(path) if filename.endswith(".py")]:
            if module == "__init__":
                continue
            try:
                self.load_module(f"{path}.{module}")
            except Exception as err:
                self.log.error(convert.traceback(err))

    async def _handle_checks(self, ctx, no_global_checks=False):
        """Reescreve o método `_handle_checks` para aceitar múltiplas verificações."""
        if no_global_checks:
            checks = ctx.command._checks
        else:
            checks = self._checks + ctx.command._checks
        if not checks:
            return True
        for predicate in checks:
            if inspect.iscoroutinefunction(predicate):
                result = await predicate(ctx)
            else:
                result = predicate(ctx)
            if not result:
                return predicate
        return True

    def add_all_checks(self):
        """Método que adiciona todas as verificações globais."""
        self.add_check(self.channels.is_enabled) # se o bot está ativado no canal
        self.add_check(checks.is_not_banned) # se o bot está ativado no canal
        self.add_check(command.cooldown) # se o usuário está com cooldown no comando

    async def event_ready(self):
        """Evento chamado quando o Bot estiver conectado e pronto."""
        self.db = await postgresql.PostgreSQL.init(config.Vars.database, loop=self.loop)
        await self.join_all_channels()
        self.load_all_modules()
        self.add_all_checks()
        self.log.info(f"{self.nick} | {len(self.channels)} canais | {len(self.commands)} comandos")

    async def global_before_hook(self, ctx):
        """Método que é chamado antes que qualquer comando esteja prestes a ser chamado."""
        await self.db.upsert(
            "users",
            pkey="id",
            values={
                "id": ctx.author.id,
                "name": ctx.author.name,
                "channel": ctx.channel.name,
                "message": ctx.message.content,
                "timestamp": ctx.message.timestamp,
                "color": ctx.author.colour,
            },
        )

    async def global_after_hook(self, ctx):
        """Método que é chamado após qualquer comando ser chamado, independentemente se falhou ou não."""
        if not hasattr(ctx, "response") and ctx.command.usage:
            # se o comando não retornar uma resposta, envia uma mensagem de como utilizá-lo
            await ctx.send(f"@{ctx.author.name}, {ctx.command.usage}")
        elif not hasattr(ctx, "response"):
            # se não tiver uma mensagem como utilizá-lo, houve um erro
            self.log.error(f'"{ctx.content}" não contém `ctx.response`')
        elif not self.channels.is_not_banword(ctx):
            # se tiver um termo banido do canal
            pass
        else:
            await ctx.send(ctx.response)

    async def event_webhook(self, data):
        """Evento que é disparado quando uma mensagem de uma assinatura de Webhook é recebida."""
        pass

    async def event_raw_pubsub(self, data):
        """Evento que dispara quando um evento de assinatura PubSub é recebido."""
        pass

    async def event_mode(self, channel, user, status):
        """Evento chamado quando um MODE é recebido do Twitch."""
        pass

    async def event_userstate(self, user):
        """Evento chamado quando um USERSTATE é recebido do Twitch."""
        pass

    async def event_raw_usernotice(self, channel, tags: dict):
        """Evento chamado quando uma USERNOTICE é recebida do Twitch."""
        pass

    async def event_usernotice_subscription(self, metadata):
        """Evento chamado quando uma assinatura USERNOTICE ou evento de nova assinatura é recebido do Twitch."""
        pass

    async def event_part(self, user):
        """Evento chamado quando um PART é recebido do Twitch."""
        pass

    async def event_join(self, user):
        """Evento chamado quando um JOIN é recebido do Twitch."""
        pass

    async def event_message(self, message):
        """Evento chamado quando um PRIVMSG é recebido do Twitch."""
        if self.channels.is_offline(message):
            # se o bot estiver desativado no canal, apenas remove o status de afk
            await afk.returned(self, message, send=False)
        elif (
            message.author.name == self.nick # se o usuário for o próprio bot
            or await afk.returned(self, message) # se o usuário estava afk
            or await remind.reminder(self, message) # se o usuário tiver um lembrete
            or await self.channels[message.channel.name].pyramid.update(message) # se for pirâmide
        ):
            pass
        else:
            # se for um comando, o executa
            await self.handle_commands(convert.case_insensitive(message))


def main():
    bot = Bobotinho()
    bot.run()


if __name__ == "__main__":
    main()
