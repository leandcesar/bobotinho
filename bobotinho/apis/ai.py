# -*- coding: utf-8 -*-
from typing import Optional

from bobotinho import aiorequests, config


class AI:
    base_url = config.ai_url
    key = config.ai_key

    @classmethod
    async def nlu(cls, text: str) -> Optional[dict]:
        url = f"{cls.base_url}/model/parse"
        params = {"token": cls.key}
        data = {"text": text}
        return await aiorequests.post(url, params=params, json=data)

    @classmethod
    async def predict(cls, text: str) -> dict:
        response = cls.nlu(text)
        intent: str = response["intent"]["name"]
        entity: Optional[str] = response["entities"][0]["value"] if response["entities"] else ""
        confidence: float = response["intent"]["confidence"]
        if intent == "nlu_fallback":
            intent = None
        elif entity and entity.startswith(
            ("o ", "a ", "do ", "da ", "no ", "na ", "em ")
        ):
            entity = entity.split(maxsplit=1)[1]
        return {"intent": intent, "entity": entity, "confidence": confidence}

    @staticmethod
    def small_talk(intent: str) -> Optional[str]:
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
