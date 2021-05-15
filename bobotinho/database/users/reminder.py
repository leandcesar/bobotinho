# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, TimestampMixin, ContentMixin, fields, timezone


class Reminder(Base, TimestampMixin, ContentMixin):
    channel = fields.ForeignKeyField("users.User", to_field="name", related_name="reminders_on")
    user_from = fields.ForeignKeyField("users.User", to_field="name", related_name="reminders_to")
    user_to = fields.ForeignKeyField("users.User", to_field="name", related_name="reminders_from")
    scheduled_for = fields.DatetimeField(null=True)

    class Meta:
        app = "users"
        table = "reminder"

    @property
    def scheduled_ago(self):
        return self.scheduled_for - timezone.now()
