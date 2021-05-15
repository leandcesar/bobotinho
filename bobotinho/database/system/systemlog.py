# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, fields


class SystemLog(Base, TimestampMixin):
    error = fields.CharField(max_length=500, null=True)

    class Meta:
        app = "system"
        table = "systemlog"
