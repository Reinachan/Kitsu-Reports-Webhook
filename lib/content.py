from typing import Optional


class Content:
    def __init__(self, content, post_id) -> None:
        self.id: Optional[str] = content["id"] or None
        self.url: Optional[str]
        self.text: Optional[str] = content["content"] or None
        self.type = content["__typename"]
        self.content = content
        self.media_title: Optional[str] = None
        self.media_poster: Optional[str] = None

        self.content_type(post_id)

    def content_type(self, post_id):
        if self.type == "MediaReaction":
            self.url = f"https://kitsu.io/media-reactions/{self.id}"
            self.media_title = self.content["media"]["titles"]["canonical"]
            self.media_title = (
                self.content["media"]["posterImage"]["original"]["url"] or None
            )

        if self.type == "Post":
            self.url = f"https://kitsu.io/posts/{self.id}"
            self.media_title = self.content["postMedia"]["titles"]["canonical"] or None
            self.media_title = (
                self.content["postMedia"]["posterImage"]["original"]["url"] or None
            )
        if self.type == "Comment":
            self.url = f"https://kitsu.io/comments/{self.id}"
