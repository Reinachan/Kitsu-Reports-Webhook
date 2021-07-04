# Imports
from lib.authentication import authentication
from typing import Literal
import requests
import json
import time
import os
import traceback
import lib.constants as constants
import lib.get_user as get_user
import lib.get_url_type as get_url_type
import lib.get_offender as get_offender
import lib.get_image as get_image
import lib.discord
import encodings

stop_code = False


def fetch_reports():
    # FETCH DATA FROM KITSU
    url = constants.url
    headers = constants.headers
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

    # FETCH PREVIOUS REQUEST
    latest_report = "0"

    if os.path.exists("reports.json"):
        with open("reports.json", "r") as read_file:
            # Convert JSON file to Python Types
            obj = json.load(read_file)

        if "data" in obj:
            if len(obj["data"]) > 0:
                latest_report = obj["data"][0]["id"]
            else:
                env.token = authentication(env.slug, env.password)
                print("39: fetching token")

    # SORT OUT TO ONLY NEW REPORTS
    new_reports = []

    if "data" in data:
        for report in data["data"]:
            try:
                if report["id"] > latest_report:
                    # Structure data for Discord
                    attr = report["attributes"]
                    rel = report["relationships"]

                    reporter = get_user.get_user(rel)

                    naughty_type = attr["naughtyType"]
                    naughty_url_type = get_url_type.get_url_type(naughty_type)

                    post_url = (
                        "https://kitsu.io/"
                        + naughty_url_type
                        + "/"
                        + str(attr["naughtyId"])
                    )

                    offender = get_offender.get_offender(
                        naughty_url_type, attr["naughtyId"]
                    )

                    offending_image = None
                    if offender:
                        offender_name = offender["included"][0]["attributes"]["name"]
                        offender_id = offender["included"][0]["id"]

                        if naughty_url_type == "media-reactions":
                            offender_text = offender["data"]["attributes"]["reaction"]
                            offender_text = json.dumps(
                                offender_text, ensure_ascii=False
                            )
                        elif naughty_url_type == "reviews":
                            offender_text = offender["data"]["attributes"]["content"]
                            offender_text = json.dumps(
                                offender_text, ensure_ascii=False
                            )
                        else:
                            offender_text = offender["data"]["attributes"]["content"]
                            offender_text = json.dumps(
                                offender_text, ensure_ascii=False
                            )
                            if offender["data"]["relationships"]["uploads"]["links"][
                                "related"
                            ]:
                                offending_image = get_image.get_image(
                                    offender["data"]["relationships"]["uploads"][
                                        "links"
                                    ]["related"]
                                )
                            else:
                                offending_image = None

                    else:
                        offender_name = "Missing"
                        offender_text = "Missing"
                        offender_id = "2"

                    description = (
                        "**Explanation**\n"
                        + str(attr["explanation"])
                        + "\n\n**Offender**\n"
                        + "["
                        + str(offender_name)
                        + "](https://kitsu.io/users/"
                        + str(offender_id)
                        + ")"
                        + "\n\n**Offense**\n"
                        + str(offender_text)
                    )

                    description = (
                        (description[:1040] + " …")
                        if len(description) > 1040
                        else description
                    )
                    print(description)

                    discord = {
                        "url": post_url,
                        "timestamp": attr["createdAt"],
                        "description": description,
                        "color": "16208182",
                        "image": {
                            "url": offending_image,
                        },
                        "author": {
                            "name": reporter["name"],
                            "url": "https://kitsu.io/admin/reports/open",
                            "icon_url": reporter["avatar"]["small"],
                        },
                        "footer": {"text": "Status: " + attr["status"]},
                        "fields": [
                            {
                                "name": "Links",
                                "value": "["
                                + attr["naughtyType"]
                                + "]("
                                + post_url
                                + ")\n"
                                + "[All Reports](https://kitsu.io/admin/reports/open)",
                                "inline": "true",
                            },
                            {
                                "name": "Reason",
                                "value": attr["reason"],
                                "inline": "true",
                            },
                        ],
                    }

                    new_reports.append(discord)
            except Exception:
                print("exception!")
                discord = {
                    "title": "Something went wrong!",
                    "description": "Here's some technobabble about it:\n```py\n"
                    + traceback.format_exc()
                    + "\n```",
                    "footer": {
                        "text": "This error almost killed the script! Don't worry. Reina's totally awesome, super-great, not at all bad coding skills gracefully handled this exception which means you'll just have to go to the website to view this report instead",
                    },
                    "fields": [
                        {
                            "name": "Links",
                            "value": "[All Reports](https://kitsu.io/admin/reports/open)",
                            "inline": "true",
                        },
                    ],
                }
                new_reports.append(discord)

    else:
        env.token = authentication(env.slug, env.password)
        print("117: fetching token")

    for nreport in new_reports[::-1]:
        to_discord = {
            "username": "Kitsu Reports",
            "url": "https://kitsu.io/admin/reports/open",
            "avatar_url": "https://avatars.githubusercontent.com/u/7648832?s=200&v=4",
            "embeds": [nreport],
        }

        # SEND NEW REPORTS TO DISCORD WEBHOOK
        disc_response = requests.post(
            env.webhook,
            headers={"Content-Type": "application/json"},
            json=to_discord,
        )

        print(disc_response)
        time.sleep(0.5)

    if "data" in data:
        # write json to disk for next comparsion
        with open("reports.json", "w") as write_file:
            json.dump(data, write_file, indent=4)
    else:
        print("148: probably invalid token or smth. No 'data' in the response")


while True:
    if env.authenticated:
        fetch_reports()
        print("Fetched")
        time.sleep(60)
    else:
        print("refreshing token")
        env.authenticated = True
        fetch_reports()
