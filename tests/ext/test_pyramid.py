# -*- coding: utf-8 -*-
import pytest

from bobotinho.ext.pyramid import Pyramid


@pytest.fixture
def pyramid():
    return Pyramid()


def test_pyramid_1(pyramid):
    assert pyramid.update("username", "content") is False
    assert len(pyramid) == 1
    assert pyramid.update("username", "content content") is False
    assert len(pyramid) == 2
    assert pyramid.update("username", "content content content") is False
    assert len(pyramid) == 3
    assert pyramid.update("username", "content content") is False
    assert len(pyramid) == 3
    assert pyramid.update("username", "content") is True
    assert len(pyramid) == 3


def test_pyramid_2(pyramid):
    assert pyramid.update("username", "content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username", "content content content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username2", "content") is False
    assert pyramid.update("username2", "content content") is False
    assert pyramid.update("username2", "content") is True
    assert len(pyramid) == 2


def test_pyramid_fail_1(pyramid):
    assert pyramid.update("username", "content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username", "content content content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username", "content content content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username", "content") is False


def test_pyramid_fail_2(pyramid):
    assert pyramid.update("username", "content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username", "content content content") is False
    assert pyramid.update("username", "content") is False


def test_pyramid_fail_3(pyramid):
    assert pyramid.update("username", "content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username", "content content content") is False
    assert pyramid.update("username", "content content") is False
    assert pyramid.update("username2", "content") is False
    assert pyramid.update("username", "content") is False
