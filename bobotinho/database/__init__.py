# -*- coding: utf-8 -*-
from tortoise import Tortoise


class Database:
    def __init__(self, urls: dict):
        self.urls = urls
        self.system_log = None

    async def init(self):
        models = ["bobotinho.database.models"]
        await Tortoise.init(
            config={
                "connections": {
                    "conn_1": self.urls["db_1"],
                    "conn_2": self.urls["db_2"],
                    "conn_3": self.urls["db_3"],
                    "conn_4": self.urls["db_4"],
                },
                "apps": {
                    "system": {"models": models, "default_connection": "conn_1"},
                    "users": {"models": models, "default_connection": "conn_2"},
                    "cookies": {"models": models, "default_connection": "conn_3"},
                    "dungeons": {"models": models, "default_connection": "conn_4"},
                },
            }
        )
        await Tortoise.generate_schemas(safe=True)

    async def close(self):
        await Tortoise.close_connections()

    async def register_init(self):
        try:
            from bobotinho.database.models import SystemLog
            self.system_log = await SystemLog.create()
        except Exception:
            pass

    async def register_close(self, e: Exception = None):
        if self.system_log:
            self.system_log.error = str(repr(e)) if e else None
            await self.system_log.save(update_fields=["error", "updated_at"])
