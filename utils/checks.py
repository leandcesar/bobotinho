# -*- coding: utf-8 -*-

import config 
import re


def is_admin(ctx):
    return is_owner(ctx) or is_mod(ctx)


def is_allowed(ctx):
    return is_owner(ctx) or is_sub(ctx) or is_vip(ctx) or is_mod(ctx)


def is_owner(ctx):
    return ctx.author.id == config.Vars.owner_id


def is_mod(ctx):
    return ctx.author.is_mod or ctx.author.name == ctx.channel.name


def is_vip(ctx):
    return ctx.author.badges.get("vip", False)


def is_sub(ctx):
    return ctx.author.is_subscriber


def is_link(message: str):
    return re.search(r"([.0-9a-zA-Z-]*\.[a-z]{2,3}(?:\/\S*))", message)
