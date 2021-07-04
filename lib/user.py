from typing import Optional


class User:
    def __init__(self, user) -> None:
        self._id = user["id"] or "1"
        self.url = "https://kitsu.io/users/" + self._id or "https://kitsu.io/users/1"
        self.name: Optional[str] = user["name"] or "Deleted"
        self.avatar: Optional[str] = self.avatar(user["avatarImage"]["original"]["url"])

    def avatar(self, avatar):
        print("AVATAR")
        try:
            if avatar == "/avatars/original/missing.png":
                return "https://kitsu.io/images/default_avatar-2ec3a4e2fc39a0de55bf42bf4822272a.png"
            if avatar == None:
                return "https://kitsu.io/images/default_avatar-2ec3a4e2fc39a0de55bf42bf4822272a.png"
            return avatar
        except:
            return "https://kitsu.io/images/default_avatar-2ec3a4e2fc39a0de55bf42bf4822272a.png"


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


class DefaultUser:
    def __init__(self) -> None:
        self._id: str = "0"
        self.url: Optional[str] = "https://kitsu.io/users/1"
        self.name: Optional[str] = "Kitsu Reports"
        self.avatar: Optional[
            str
        ] = "https://kitsu.io/images/default_avatar-2ec3a4e2fc39a0de55bf42bf4822272a.png"
