from flask_login import current_user

from blog import db
from blog.post.models import Comment, Post


def save_changes(obj: db.Model):
    """
    Add and commit changes to DB
    :param obj: Flask model
    :type obj: db.Model
    """

    db.session.add(obj)
    db.session.commit()


def get_all_posts() -> list:
    """
    Get list of posts
    :return: List of posts
    :rtype: list
    """

    return Post.query.order_by(Post.created.desc()).all()


def create_post(data: dict) -> Post:
    """
    Create a new post
    :param data: Fields of new record
    :type data: dict
    :return: Created post model
    :rtype: Post
    """

    post = Post(**data)
    post.user_id = current_user.id
    post.generate_slug()

    save_changes(obj=post)

    return post


def get_post(slug: str) -> Post:
    """
    Get specific post
    :param slug: Post's slug
    :type slug: str
    :return: Found post
    :rtype: Post
    """

    return Post.query.filter_by(slug=slug).one()


def delete_post(slug: str):
    """
    Delete specific post
    :param slug: Post's identifier
    :type slug: str
    """

    Post.query.filter_by(slug=slug).delete()
    db.session.commit()


def change_post(slug: str, data: dict) -> Post:
    """
    Change specific post
    :param slug: Post's identifier
    :type slug: str
    :param data: Fields of new record
    :type data: dict
    :return: Changed post model
    :rtype: Post
    """

    post = get_post(slug)
    post.title = data["title"]
    post.body = data["body"]
    post.generate_slug()

    save_changes(obj=post)

    return post


def like_post(slug: str) -> Post:
    """
    Like a specific post
    :param slug: Post's identifier
    :type slug: str
    :return: Liked post model
    :rtype: Post
    """

    post = get_post(slug)
    post.like(current_user.id)

    return post


def dislike_post(slug: str) -> Post:
    """
    Dislike a specific post
    :param slug: Post's identifier
    :type slug: str
    :return: Disliked post model
    :rtype: Post
    """

    post = get_post(slug)
    post.dislike(current_user.id)

    return post


def comment_post(slug: str, data: dict) -> Post:
    """
    Comment a specific post
    :param slug: Post's identifier
    :type slug: str
    :param data: Fields of comment
    :type data: dict
    :return: Commented post model
    :rtype: Post
    """

    comment = Comment(**data)
    post = get_post(slug)
    post.comments.append(comment)

    save_changes(obj=post)

    return post


def get_comment(comment_id: int) -> Comment:
    """
    Get specific comment
    :param comment_id: Comment's identifier
    :type comment_id: int
    :return: Found comment
    :rtype: Comment
    """

    return Comment.query.filter_by(id=comment_id).one()


def like_comment(comment_id: int) -> Comment:
    """
    Like a specific comment
    :param comment_id: Post's identifier
    :type comment_id: int
    :return: Liked comment model
    :rtype: Comment
    """

    comment = get_comment(comment_id)
    comment.like(current_user.id)

    return comment


def dislike_comment(comment_id: int) -> Comment:
    """
    Dislike a specific comment
    :param comment_id: Post's identifier
    :type comment_id: int
    :return: Disliked comment model
    :rtype: Comment
    """

    comment = get_comment(comment_id)
    comment.dislike(current_user.id)

    return comment
