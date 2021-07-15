# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, ContentMixin, TimestampMixin, fields


class Suggest(Base, TimestampMixin, ContentMixin):
    name = fields.CharField(max_length=64, description="Twitch username")
    channel = fields.CharField(max_length=64, description="Twitch username")

    class Meta:
        app = "system"
        table = "suggest"
