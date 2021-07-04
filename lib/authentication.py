import requests
import json
import os


def authentication():
    auth = os.environ.get("AUTHENTICATION")
    username = os.environ.get("KITSU_USERNAME")
    password = os.environ.get("KITSU_PASSWORD")

    if auth:
        return auth

    else:
        get_auth = requests.post(
            "https://kitsu.io/api/oauth/token",
            headers={
                "Accept": "application/vnd.api+json",
                "Content-Type": "application/vnd.api+json",
            },
            json={
                "grant_type": "password",
                "username": username,
                "password": password,  # RFC3986 URl encoded string
            },
        )
        get_auth = json.loads(get_auth.text)

        os.environ["AUTHENTICATION"] = get_auth["access_token"]

        return os.environ["AUTHENTICATION"]
