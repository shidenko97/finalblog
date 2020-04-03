from datetime import datetime

from slugify import UniqueSlugify

from blog import db


class LikableModel:
    """Special implement of likes/dislikes"""

    id = None
    "Identifier of object"

    like_model = None
    "Like class for object"

    like_model_fk = None
    "Foreign key to like model"

    def get_user_mark(self, user_id: int):
        """
        Get user's mark of object in object view
        :param user_id: User identifier
        :type user_id: int
        :return: Mark object
        """

        return (self.like_model
                .query
                .filter_by(**{self.like_model_fk: self.id, "user_id": user_id})
                .first())

    def like(self, user_id: int) -> bool:
        """
        Like the object
        :param user_id: User identifier
        :type user_id: int
        :return: Result of like
        :rtype: bool
        """

        return self._mark_it(user_id, True)

    def dislike(self, user_id: int) -> bool:
        """
        Dislike the object
        :param user_id: User identifier
        :type user_id: int
        :return: Result of dislike
        :rtype: bool
        """

        return self._mark_it(user_id, False)

    def likes_count(self) -> int:
        """
        Get count of object's likes
        :return: Count of likes
        :rtype: int
        """

        return (self.like_model
                .query
                .filter_by(**{self.like_model_fk: self.id, "sign": True})
                .count())

    def dislikes_count(self) -> int:
        """
        Get count of object's dislikes
        :return: Count of dislikes
        :rtype: int
        """

        return (self.like_model
                .query
                .filter_by(**{self.like_model_fk: self.id, "sign": False})
                .count())

    def _mark_it(self, user_id: int, sign: bool) -> bool:
        """
        Mark the object
        :param user_id: User identifier
        :type user_id: int
        :param sign: Sign of mark (True - like, False - dislike)
        :type sign: bool
        :return: Result of mark
        :rtype: bool
        """

        result = True
        mark = self.get_user_mark(user_id)

        if mark is None:
            # User's mark doesn't exists - create it
            mark = self.like_model(**{
                self.like_model_fk: self.id,
                "user_id": user_id,
                "sign": sign
            })
            db.session.add(mark)
        elif sign != mark.sign:
            # User's mark is reverse - change it
            mark.sign = sign
            db.session.add(mark)
        else:
            # User's mark exists - delete it
            db.session.delete(mark)
            result = False

        db.session.commit()

        return result


class PostLike(db.Model):
    """Model for post's likes"""

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    sign = db.Column(db.Boolean, index=True)


class CommentLike(db.Model):
    """Model for comment's likes"""

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    sign = db.Column(db.Boolean, index=True)


class Comment(db.Model, LikableModel):
    """Model for comments"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), index=True)
    body = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.now())
    marks = db.relationship('CommentLike', backref='comment', lazy="dynamic")
    user = db.relationship('User', backref='comments', lazy=True)

    # Parameters for Likable model
    like_model = CommentLike
    like_model_fk = "comment_id"


class Post(db.Model, LikableModel):
    """Model for posts"""

    POSTS_PER_PAGE = 10
    """Posts per page for pagination"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
    title = db.Column(db.String(64))
    slug = db.Column(db.String(64), index=True, unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    comments = db.relationship('Comment', backref='post', lazy="dynamic",
                               order_by=Comment.datetime.desc())
    marks = db.relationship('PostLike', backref='post', lazy="dynamic")
    user = db.relationship('User', backref='posts', lazy=True)

    # Parameters for Likable model
    like_model = PostLike
    like_model_fk = "post_id"

    def __repr__(self):
        return f"[id: {self.id}] {self.title}"

    def generate_slug(self):
        """Create unique slug from title"""

        all_slugs = Post.query.with_entities(Post.slug).all()

        if self.title:
            custom_slugify = UniqueSlugify(to_lower=True,
                                           uids=[slug for slug, in all_slugs])
            self.slug = custom_slugify(self.title)
