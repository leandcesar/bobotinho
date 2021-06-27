# -*- coding: utf-8 -*-
import os

from bobotinho import aiorequests
from bobotinho.logger import log


class AI:
    base_url = os.getenv("BOT_AI_URL")
    key = os.getenv("BOT_AI_KEY")

    @classmethod
    async def nlu(cls, text: str) -> dict:
        url = f"{cls.base_url}/model/parse"
        params = {"token": cls.key}
        data = {"text": text}
        try:
            response = await aiorequests.post(url, params=params, json=data)
            intent = response["intent"]["name"]
            entity = response["entities"][0]["value"] if response["entities"] else None
            # TODO: mudar nlu pra não capturar pronomes nas entities
            if entity and entity.startswith(
                ("o ", "a ", "do ", "da ", "no ", "na ", "em ")
            ):
                entity = entity.split(maxsplit=1)[1]
            return {"intent": intent, "entity": entity}
        except Exception as e:
            log.exception(e)
        return {"intent": None, "entity": None}

    @staticmethod
    def is_small_talk(response: dict) -> bool:
        return response["intent"] in (
            "nlu_fallback", "ping", "greet", "how_are_you", "who_are_you", "praise", "swear"
        )

    @staticmethod
    def response(intent: str) -> str:
        if intent == "ping":
            return "estou aqui"
        elif intent == "greet":
            return "oi"
        elif intent == "how_are_you":
            return "estou bem"
        elif intent == "who_are_you":
            return 'eu sou um bot, veja meus comandos digitando "%help"'
        elif intent == "praise":
            return "😊"
        elif intent == "swear":
            return "🖕"
        return 'não entendi isso, mas tente ver meus comandos digitando "%help"'
