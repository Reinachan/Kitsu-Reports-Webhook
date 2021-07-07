from lib.helpers.create_basic_json import create_basic_json
from lib.helpers.test import test
from lib.helpers.components import components
from typing import Optional, Union
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

        self.report_id = report._id
        self.message_id: Union[str, None] = None
        self.explanation = report.explanation
        self.url = os.environ["DISCORD_HOOK"]

        self.exists = False
        self.current_report: Union[str, None]

        self.report = report

        self.check_existing()

        if self.exists:
            self.update_report()
        else:
            self.post(None)
            self.create_store()

    def check_existing(self):
        reports = self.open_reports()
        for report in reports["reports"]:
            if report["id"] == self.report_id:
                self.exists = True
                self.current_report = report
                return reports

    def open_reports(self) -> Union[dict, None]:
        if not os.path.exists("reports.json"):
            create_basic_json()

        with open("reports.json", "r") as read_file:
            # Convert JSON file to Python Types
            return json.load(read_file)

    def create_store(self):
        save = {
            "id": self.report._id,
            "discord": self.message_id or "0",
            "status": self.report.status,
        }
        exists = self.exists
        opened = self.open_reports()

        if not opened:
            self.store(
                [],
                save,
            )
        elif not exists:
            self.store(opened["reports"], save)

    def store(self, existing: list, results: dict):
        with open("reports.json", "w") as write_file:
            report_list = existing
            if results:
                report_list.append(results)
            reports = {"reports": report_list}

            write_file.write(json.dumps(reports))

    def naughty_type(self):
        if self.report.type == "MediaReaction":
            return

    def post(self, url):
        query = {
            "wait": "true",
            "Authorization": os.environ["DISCORD_BEARER"],
        }

        try:
            content = self.report.content.text or ""
        except:
            content = ""

        try:
            thumb_url = self.report.content.media_poster
        except:
            thumb_url = ""

        try:
            content_link = self.report.content.url
        except:
            content_link = ""

        description = content

        if self.report.moderator.name == "Kitsu Reports":
            moderator = ""
        else:
            moderator = self.report.moderator.name + " -"

        reason = self.report.reason.title()

        payload = {
            "username": f"{self.username}",
            "avatar_url": f"{self.avatar_url}",
            "content": f"{self.explanation}",
            "embeds": [
                {
                    "author": {
                        "name": self.report.naughty.name,
                        "icon_url": self.report.naughty.avatar,
                        "url": self.report.naughty.url,
                    },
                    "title": self.report.type,
                    "description": description,
                    "footer": {
                        "text": f"{moderator} {self.report.status}",
                        "icon_url": self.report.moderator.avatar,
                    },
                    "thumbnail": {"url": thumb_url},
                    "fields": [
                        {
                            "name": "Reason      ",
                            "value": reason,
                            "inline": "true",
                        },
                        {
                            "name": "links",
                            "value": f"[{self.report.type}]({content_link})\n[All Reports](https://kitsu.io/admin/reports/open)",
                            "inline": "true",
                        },
                    ],
                    "components": [
                        {
                            "type": 1,
                            "components": [
                                {
                                    "type": 2,
                                    "label": self.report.type,
                                    "style": 5,
                                    "url": content_link,
                                },
                                {
                                    "type": 2,
                                    "label": self.report.naughty.name,
                                    "style": 5,
                                    "url": "",
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

        if url:
            response = requests.patch(url, json=payload)

        else:
            response = requests.post(self.url, params=query, json=payload)

        # self.message_id = response.json()["id"]

        res: dict = json.loads(response.text)
        self.message_id = res.get("id") or "0"

        time.sleep(1.2)

    def update_report(self):
        status = self.current_report["status"]
        if status != self.report.status:

            self.post(self.url + "/messages/" + self.current_report["discord"])

            self.update_status()

    def update_status(self):
        opened = self.open_reports()
        for report in opened["reports"]:
            if report["id"] == self.report_id:
                report["status"] = self.report.status

        save = None
        exists = self.exists

        self.store(opened["reports"], save)
