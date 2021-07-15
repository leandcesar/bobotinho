# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, ContentMixin, fields, timezone


class Reminder(Base, TimestampMixin, ContentMixin):
    from_user_id = fields.IntField()
    to_user_id = fields.IntField()
    channel_id = fields.IntField()
    scheduled_for = fields.DatetimeField(null=True)

    class Meta:
        app = "system"
        table = "reminder"

    @property
    def scheduled_ago(self):
        return self.scheduled_for - timezone.now()
