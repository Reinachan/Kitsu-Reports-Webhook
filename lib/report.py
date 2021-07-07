import json
from sqlite3.dbapi2 import Connection, Cursor
from lib.content import Content
from lib.discord import Discord
from lib.user import DefaultUser, Moderator, NaughtyUser, Reporter
from lib.authentication import authentication
from typing import Optional, Text
import requests
import os
from lib.fetch_graphql import get_reports
import sqlite3


def fetch_reports(db: Connection):
    auth_token = authentication()

    reports = get_reports(auth_token)

    print(reports)

    for report in reports["reports"]["nodes"][::-1]:
        rep = Report(report, db)

        print("\n")
        # for attr in rep.__dict__:
        #     print(f"{attr} -> {getattr(rep, attr)}")


class Report:
    def __init__(self, report: dict, db: Connection) -> None:
        self.report = report
        self._id: str = report["id"]
        self.explanation: Optional[str] = report["explanation"] or None
        self.reason: Optional[str] = report["reason"] or None
        self.status: Optional[str] = report["status"] or None
        self.type: Optional[str] = report["naughty"]["__typename"] or None

        self.moderator = self.init_moderator(report["moderator"])
        self.reporter = self.init_reporter(report["reporter"])
        self.naughty = self.init_naughty(report["naughty"]["author"])
        self.content = self.init_content(report["naughty"])

        # self.database_query(report, db)

        # cursor = db.cursor()

        # if self.exists_in_database(cursor):
        #     self.post_reports(cursor)

    def create_number(self, _id):
        with open("reports.json", "w") as write_file:
            json.dump({"id": _id}, write_file, indent=4)

    def exists_in_database(self, db: Cursor):
        query = db.execute("SELECT * FROM report where report_id = " + self._id)
        query = query.fetchall()
        if not query:
            self.database_query(self.report, db)
        else:
            return query

    def database_query(self, report, db: Cursor):
        content = "NULL, NULL, NULL, NULL"
        try:
            if self.type == "Comment":
                content = f"NULL,{self.content.id},NULL,NULL"
            elif self.type == "Post":
                content = f"{self.content.id},NULL,NULL,NULL"
            elif self.type == "Reaction":
                content = f"NULL,NULL,{self.content.id},NULL"
            elif self.type == "Review":
                content = f"NULL,NULL,NULL,{self.content.id}"
        except:
            content = "NULL, NULL, NULL, NULL"

        # insert = db.execute(
        #     f"INSERT INTO report VALUES ({self._id}, {self.explanation}, {self.type}, {self.status}, {self.reporter._id}, {self.naughty._id}, {self.moderator._id}, {content}, NONE)"
        # )

        # return query if query else cursor.execute(f"INSERT INTO report VALUES ({_id}, {})")

        # results = cursor.fetchall()

    def init_moderator(self, moderator):
        try:
            return Moderator(moderator)
        except:
            return DefaultUser()

    def init_reporter(self, reporter):
        try:
            return Reporter(reporter)
        except:
            return DefaultUser()

    def init_naughty(self, naughty):
        try:
            return NaughtyUser(naughty)
        except:
            return DefaultUser()

    def init_content(self, content):
        try:
            return Content(content, self._id)
        except:
            return None

    def post_reports(self):
        if os.path.exists("reports.json"):
            with open("reports.json", "r") as read_file:
                # Convert JSON file to Python Types
                obj = json.load(read_file)

            if "id" in obj and obj["id"] < self._id:
                Discord(self)
                self.create_number()
