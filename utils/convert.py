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

import re
import traceback as tb

from datetime import datetime
from typing import Union
from twitchio.dataclasses import Message
from utils import time


def case_insensitive(message: Message, prefix: str = "%") -> Message:
    """Converte o comando de uma mensagem para minúsculo, se houver.

    Argumentos:
    message -- mensagem <class 'twitchio.dataclasses.Message'>
    prefix -- prefixo do bot (default %)
    """
    if message.content.startswith(prefix) and len(message.content) > 1:
        content = message.content.replace("󠀀", "")  # remove caractere invisível
        if content[1] == " ":
            content = content[0] + content[2:]
        try:
            index = content.index(" ")
            message.content = content[:index].lower() + content[index:]
        except:
            message.content = content.lower()
    return message


def command(target: str, prefix: str = "%") -> str:
    """Converte o nome do comando, se válido, para minúsculo e remove o prefixo do início.

    Argumentos:
    target -- nome do comando
    prefix -- prefixo do bot (default %)
    """
    if target[0] == prefix and len(target) > 1:
        target = target[1:]
    if not target.isalnum() and target != "%":
        return ""
    return target.lower()


def user(target: str) -> str:
    """Converte o nome de usuário para minúsculo e remove '@' do início e ',' do fim.

    Argumentos:
    target -- nome do usuário
    """
    if target[0] == "@":
        target = target[1:]
    if target[-1] == ",":
        target = target[:-1]
    return target.lower()


def number(target: Union[int, float]) -> str:
    """Atribui vírgula como separador decimal e ponto como agrupador de milhares para um número.

    Argumentos:
    target -- número inteiro ou decimal
    """
    if float(target) > 1e15:
        raise ValueError(f"Expected value less than 1e15, but {target} was given")
    elif isinstance(target, int):
        return f"{target:,d}".replace(",", ".")
    elif isinstance(target, float):
        return f"{target:,.2f}"[::-1].replace(",", ".").replace(".", ",", 1)[::-1]


def date(target) -> datetime:
    """Converte a entrada para <class 'datetime.datetime'>.
    
    Argumentos:
    target -- data, hora, data e hora, ou número que represente tempo
    """
    return time.parse_date(target)


def cooldown(target, duration, now=None) -> Union[str, bool]:
    """Calcula o tempo restante para um cooldown acabar. Se tiver acabado, retorna False.

    Argumentos:
    target -- data e/ou hora alvo
    cooldown -- duração do cooldown
    now -- data e/ou hora; se None, utiliza a data e hora atuais (default None)
    """
    return timesince(target, now=now, cooldown=duration)


def timesince(target, **kwargs) -> Union[str, bool]:
    """Calcula a diferença entre uma data e/ou hora com a data e hora atuais.

    Argumentos:
    target -- data e/ou hora alvo

    Opcionais:
    cooldown -- duração do cooldown, caso deseje-se calcular o tempo restante para 
            liberar um comando
    future -- indica se espera-se que 'target' esteja no futuro com relação 
            a 'now' (default False)
    now -- data e/ou hora base; se None, utiliza a data e hora atuais (default None)
    """
    cooldown = kwargs.pop("cooldown", None)
    future = kwargs.pop("future", False)
    now = kwargs.pop("now", None)

    target = time.parse_date(target)
    now = time.parse_date(now) if now else time.datetime.datetime.utcnow()
    
    if (target > now) != future:
        return False
    
    delta = target - now if future else now - target

    if cooldown:
        cooldown = time.parse_delta(cooldown)
        if delta > cooldown:
            # cooldown terminou
            return False
        return time.date_format(cooldown - delta)    
    return time.date_format(delta)


def traceback(err: Exception) -> str:
    """Converte uma exceção um relatório de rastreamento das chamadas de função feitas.

    Argumentos:
    err -- exceção gerada no código
    """
    format_tb = "".join(tb.format_tb(err.__traceback__))
    return f"{format_tb}{type(err).__name__}: {err}"
