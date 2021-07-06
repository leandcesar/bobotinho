# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, ContentMixin, fields


class Afk(Base, TimestampMixin, ContentMixin):
    user_id = fields.IntField()
    alias = fields.CharField(max_length=8, null=True)

    class Meta:
        app = "users"
        table = "afk"
