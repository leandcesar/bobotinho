# -*- coding: utf-8 -*-
import pytest
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(["bobotinho.database.models"], db_url="sqlite://:memory:")
    request.addfinalizer(finalizer)
