# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, session
from requests_oauthlib import OAuth2Session

from bobotinho import aiorequests, bot_config
from bobotinho.database.models import Channel, User
from bobotinho.logger import log

app = Flask(__name__)


@app.get("/ping")
def ping():
    return "Pong!", 200


@app.route("/invite")
def invite():
    oauth = OAuth2Session(client_id=bot_config.client_id, redirect_uri=bot_config.validate_url)
    authorization_url, state = oauth.authorization_url(f"{bot_config.oauth2_url}/authorize")
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/validating")
async def validating():
    try:
        token = await aiorequests.post(
            f"{bot_config.oauth2_url}/token",
            data={
                "grant_type": "authorization_code",
                "bot_config.client_id": bot_config.client_id,
                "bot_config.client_secret": bot_config.client_secret,
                "redirect_uri": bot_config.validate_url,
                "code": request.args.get("code"),
            },
        )
        access_token = token.get("access_token")
        user_info = await aiorequests.get(
            f"{bot_config.oauth2_url}/validate",
            headers={"Authorization": f"OAuth {access_token}"}
        )
        follows = await aiorequests.get(
            f"{bot_config.oauth2_url}/users/follows",
            params={"to_id": user_info["user_id"]},
            headers={"Client-ID": bot_config.client_id, "Authorization": f"Bearer {access_token}"},
        )
        user = await User.get_or_create(id=user_info["user_id"], name=user_info["login"].lower())
        await Channel.get_or_create(user=user, followers=follows["total"])
        return redirect(bot_config.success_url)
    except Exception as e:
        log.error(e)
        return redirect(bot_config.failed_url)
