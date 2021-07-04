from typing import Optional


class User:
    def __init__(self, user) -> None:
        self._id: str = user["id"]
        self.url: Optional[str] = "https://kitsu.io/users/" + self._id or None
        self.name: Optional[str] = user["name"] or None
        self.avatar: Optional[str] = (
            user["avatarImage"]["original"]["url"]
            or "https://kitsu.io/images/default_avatar-2ec3a4e2fc39a0de55bf42bf4822272a.png"
        )


class Moderator(User):
    def __init__(self, u_id):
        super().__init__(u_id)


class Reporter(User):
    def __init__(self, u_id):
        super().__init__(u_id)


class NaughtyUser(User):
    def __init__(self, u_id):
        super().__init__(u_id)
        self.past_names: Optional[str]
