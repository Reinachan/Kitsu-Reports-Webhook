from typing import Optional


class Content:
    def __init__(self, content) -> None:
        self.id: Optional[str] = content["id"] or ""
        self.url: Optional[str]
        self.text: Optional[str] = content["content"] or ""
        self.type = content["__typename"]
        self.content = content
        self.media_title: Optional[str] = ""
        self.media_poster: Optional[str] = ""

        self.content_type()

    def content_type(self):
        if self.type == "Comment":
            self.url = f"https://kitsu.io/comments/{self.id}"
        elif self.type == "MediaReaction":
            self.url = f"https://kitsu.io/media-reactions/{self.id}"
            self.media_title = self.content["media"]["titles"]["canonical"]
            self.media_title = (
                self.content["media"]["posterImage"]["original"]["url"] or ""
            )
        elif self.type == "Post":
            try:
                self.url = f"https://kitsu.io/posts/{self.id}"
            except:
                self.url = ""
            try:
                self.media_title = (
                    self.content["postMedia"]["titles"]["canonical"] or ""
                )
            except:
                self.media_title = ""
            try:
                self.media_title = (
                    self.content["postMedia"]["posterImage"]["original"]["url"] or ""
                )
            except:
                self.media_title = ""
