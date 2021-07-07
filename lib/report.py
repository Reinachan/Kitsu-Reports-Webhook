from lib.content import Content
from lib.discord import Discord
from lib.user import DefaultUser, Moderator, NaughtyUser, Reporter
from lib.authentication import authentication
from typing import Optional
from lib.fetch_graphql import get_reports


def fetch_reports():
    auth_token = authentication()

    reports = get_reports(auth_token)

    print(reports)

    for report in reports["reports"]["nodes"][::-1]:
        rep = Report(report)


class Report:
    def __init__(self, report: dict) -> None:
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

        self.post_reports()

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
            return Content(content)
        except:
            return None

    def post_reports(self):
        Discord(self)
