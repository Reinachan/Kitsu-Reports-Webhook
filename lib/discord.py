from lib.helpers.components import components
from typing import Optional
import requests
import os
import json
import time


# def discord(message):
#     disc_response = requests.post(
#         hook,
#         headers={"Content-Type": "application/json"},
#         json=message,
#     )
#     return disc_response


class Discord:
    def __init__(self, report) -> None:
        self.username = report.reporter.name or "Kitsu Reports"
        self.avatar_url = (
            report.reporter.avatar
            or "https://avatars.githubusercontent.com/u/7648832?s=200&v=4"
        )

        self.message_id: Optional[str]
        self.explanation = report.explanation
        self.url = os.environ["DISCORD_HOOK"]

        self.report = report

        self.post()

    def naughty_type(self):
        if self.report.type == "MediaReaction":
            return

    def post(self):
        query = {
            "wait": "true",
            "Authorization": "sIYuxm30lkHt9Ex0UPfzQ00O6C4WcmG3UIhg6WMQtfTvkxSLl4b_wfRnsBbGnq62tpr_",
        }

        try:
            content = self.report.content.text
        except:
            content = None

        try:
            thumb_url = self.report.content.media_poster
        except:
            thumb_url = None

        try:
            content_link = self.report.content.url
        except:
            content_link = None

        description = f"{content}"

        payload = {
            "username": self.username,
            "avatar_url": self.avatar_url,
            "content": self.explanation,
            "embeds": [
                {
                    "author": {
                        "name": self.report.naughty.name,
                        "icon_url": self.report.naughty.avatar,
                    },
                    "title": self.report.type,
                    "description": description,
                    "provider": {
                        "name": "TEST",
                        "url": "https://kitsu.io",
                    },
                    "footer": {
                        "text": f"{self.report.moderator.name} - {self.report.status}",
                        "icon_url": self.report.moderator.avatar,
                    },
                    "thumbnail": {"url": thumb_url},
                    "fields": [
                        {
                            "name": self.report.type,
                            "value": f"[link]({content_link})",
                        },
                        {
                            "name": "All Reports",
                            "value": "[link](https://kitsu.io/admin/reports)",
                        },
                    ],
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 2,
                                    "label": "AJZ",
                                    "style": 5,
                                    "url": "https://kitsu.io/users/657435",
                                },
                                {
                                    "type": 2,
                                    "label": "All Reports",
                                    "style": 5,
                                    "url": "https://kitsu.io/admin/reports",
                                },
                            ],
                        }
                    ],
                }
            ],
        }

        response = requests.post(self.url, params=query, json=payload)

        # self.message_id = response.json()["id"]

        print(response)

        time.sleep(1)


# li = {
#     "components": [
#         {
#             "type": 2,
#             "label": "All Reports",
#             "style": 5,
#             "url": "https://kitsu.io/admin/reports",
#         },
#         {"type": 2, "label": "AJZ", "style": 5, "url": "https://kitsu.io/users/657435"},
#     ]
# }
