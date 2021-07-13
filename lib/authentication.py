import requests
import json
import os
from datetime import datetime
import time


def token_expired():
    expiry = (
        float(os.environ.get("AUTH_EXPIRATION"))
        if os.environ.get("AUTH_EXPIRATION")
        else 0.00
    )
    now = datetime.now().timetuple()

    # Assume it's two minutes into the future as it's better
    # to fetch too early than too late.
    unix_now = time.mktime(now) + 120.0

    if expiry >= unix_now:
        print("not expired")
        return False
    print("expired")
    return expiry


def token_expiry(req):
    expires = float(req["expires_in"])

    now = datetime.now().timetuple()
    unix_now = time.mktime(now)

    os.environ["AUTH_EXPIRATION"] = str(unix_now + expires)

    print("expires at:", unix_now + expires)


def refresh_token():
    refresh = os.environ.get("REFRESH_TOKEN")

    print("refreshed")

    req = requests.post(
        "https://kitsu.io/api/oauth/token",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh,
        },
    )
    return json.loads(req.text)


def get_token():
    username = os.environ.get("KITSU_USERNAME")
    password = os.environ.get("KITSU_PASSWORD")

    print("got token")

    req = requests.post(
        "https://kitsu.io/api/oauth/token",
        headers={
            "Content-Type": "application/json",
        },
        json={
            "grant_type": "password",
            "username": username,
            "password": password,  # RFC3986 URl encoded string
        },
    )
    return json.loads(req.text)


def set_environment(req):
    os.environ["AUTHENTICATION"] = req["access_token"]
    os.environ["REFRESH_TOKEN"] = req["refresh_token"]

    print("set environment")

    return os.environ["AUTHENTICATION"]


def authentication():  # sourcery skip: remove-redundant-if
    auth = os.environ.get("AUTHENTICATION")
    refresh_t = os.environ.get("REFRESH_TOKEN")

    expired = token_expired()

    if auth and not expired:
        return auth

    if auth and expired and refresh_t:
        refresh = refresh_token()
        token_expiry(refresh)
        return set_environment(refresh)

    get_auth = get_token()
    token_expiry(get_auth)
    return set_environment(get_auth)
