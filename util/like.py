from util.database import Posts


def like(username: str, id: int, post: Posts):
    # check if the user has already liked the post or not:
    document = post.getPost(id)     #document is NONE for some reason, this function is called by handleLike, in server.py
    liked_by_list = document["liked_by"]

    if username in liked_by_list:
        already_liked = True
    else:
        already_liked = False

    return post.likePost(id, username, already_liked)
    # change the heart image on the html file accordingly