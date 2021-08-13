# -*- coding: utf-8 -*-
from tortoise import Tortoise


class Database:
    def __init__(self, url: str):
        self.url = url
        self.system_log = None

    async def init(self):
        models = ["bobotinho.database.models"]
        await Tortoise.init(db_url=self.url, modules={"models": models})
        await Tortoise.generate_schemas(safe=True)
        try:
            from bobotinho.database.models import SystemLog
            self.system_log = await SystemLog.create()
        except Exception:
            pass

    async def close(self, e: Exception = None):
        if self.system_log:
            self.system_log.error = str(repr(e)) if e else None
            await self.system_log.save(update_fields=["error", "updated_at"])
        await Tortoise.close_connections()
