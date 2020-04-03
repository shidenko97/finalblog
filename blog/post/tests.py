import unittest

from blog import db
from blog.auth.models import Role, User
from blog.post.models import Comment, Post
from blog.util.test_template import TestTemplate


class PostModelCase(TestTemplate):
    """Unit tests for Post model"""

    def test_slug(self):
        """Test slugyfing"""

        post = Post(title="Test - .+?=~! the post 123")
        post.generate_slug()

        self.assertEqual("test-the-post-123", post.slug)

    def test_slug_unique(self):
        """"""

        post1 = Post(title="Test unique slug")
        post1.generate_slug()

        db.session.add(post1)
        db.session.commit()

        post2 = Post(title="Test unique slug")
        post2.generate_slug()

        self.assertEqual("test-unique-slug-1", post2.slug)

    def test_post_like(self):
        """Test liking"""

        user_id = create_user()

        post = Post(title="Test like")

        db.session.add(post)
        db.session.commit()

        self.assertEqual((0, 0), (post.likes_count(), post.dislikes_count()))

        post.like(user_id)

        self.assertEqual(True,
                         post.marks.filter_by(user_id=user_id).one().sign)

        self.assertEqual((1, 0), (post.likes_count(), post.dislikes_count()))

        post.like(user_id)

        self.assertEqual((0, 0), (post.likes_count(), post.dislikes_count()))

    def test_post_dislike(self):
        """Test disliking"""

        user_id = create_user()

        post = Post(title="Test dislike")

        db.session.add(post)
        db.session.commit()

        self.assertEqual((0, 0), (post.likes_count(), post.dislikes_count()))

        post.dislike(user_id)

        self.assertEqual(False,
                         post.marks.filter_by(user_id=user_id).one().sign)

        self.assertEqual((0, 1), (post.likes_count(), post.dislikes_count()))

        post.dislike(user_id)

        self.assertEqual((0, 0), (post.likes_count(), post.dislikes_count()))

    def test_post_change_sign(self):
        """Test change of mark's sign"""

        user_id = create_user()

        post = Post(title="Test dislike")

        db.session.add(post)
        db.session.commit()

        post.like(user_id)

        self.assertEqual((1, 0), (post.likes_count(), post.dislikes_count()))

        post.dislike(user_id)

        self.assertEqual((0, 1), (post.likes_count(), post.dislikes_count()))


class CommentModelCase(TestTemplate):
    """Unit tests for Comment model"""

    def test_comment_like(self):
        """Test liking"""

        user_id = create_user()

        comment = Comment(body="Test comment")
        post = Post(title="Test dislike")
        post.comments.append(comment)

        db.session.add_all([post, comment])
        db.session.commit()

        self.assertEqual((0, 0),
                         (comment.likes_count(), comment.dislikes_count()))

        comment.like(user_id)

        self.assertEqual(True,
                         comment.marks.filter_by(user_id=user_id).one().sign)

        self.assertEqual((1, 0),
                         (comment.likes_count(), comment.dislikes_count()))

        comment.like(user_id)

        self.assertEqual((0, 0),
                         (comment.likes_count(), comment.dislikes_count()))

    def test_comment_dislike(self):
        """Test disliking"""

        user_id = create_user()

        comment = Comment(body="Test comment")
        post = Post(title="Test dislike")
        post.comments.append(comment)

        db.session.add_all([post, comment])
        db.session.commit()

        self.assertEqual((0, 0),
                         (comment.likes_count(), comment.dislikes_count()))

        comment.dislike(user_id)

        self.assertEqual(False,
                         comment.marks.filter_by(user_id=user_id).one().sign)

        self.assertEqual((0, 1),
                         (comment.likes_count(), comment.dislikes_count()))

        comment.dislike(user_id)

        self.assertEqual((0, 0),
                         (comment.likes_count(), comment.dislikes_count()))

    def test_comment_change_sign(self):
        """Test change of mark's sign"""

        user_id = create_user()

        comment = Comment(body="Test comment")
        post = Post(title="Test dislike")
        post.comments.append(comment)

        db.session.add_all([post, comment])
        db.session.commit()

        comment.like(user_id)

        self.assertEqual((1, 0),
                         (comment.likes_count(), comment.dislikes_count()))

        comment.dislike(user_id)

        self.assertEqual((0, 1),
                         (comment.likes_count(), comment.dislikes_count()))


def create_user() -> int:
    """
    Creates a user and return his id
    :return: ID of created user
    :rtype: int
    """

    role = Role(name="User")
    user = User(fullname="Test Test", email="test@test.test")
    user.roles.append(role)

    db.session.add_all([role, user])
    db.session.commit()

    return user.id


if __name__ == "__main__":
    unittest.main()
