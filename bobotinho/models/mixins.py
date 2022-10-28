# -*- coding: utf-8 -*-
from datetime import datetime

from pynamodb.attributes import UTCDateTimeAttribute


class DateTimeMixin:
    created_on = UTCDateTimeAttribute(null=True, default_for_new=datetime.utcnow(), attr_name="co")
    updated_on = UTCDateTimeAttribute(null=True, default=datetime.utcnow(), attr_name="uo")
