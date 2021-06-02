def get_url_type(ntype):
    if ntype == "Post":
      return "posts"
    elif ntype == "Comment":
      return "comments"
    elif ntype == "MediaReaction":
      return "media-reactions"
    elif ntype == "Review":
      return "reviews"