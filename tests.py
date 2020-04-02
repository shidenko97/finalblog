import unittest

# Import tests from all modules
from blog.auth.tests import UserModelCase  # noqa: F401
from blog.post.tests import CommentModelCase, PostModelCase  # noqa: F401


if __name__ == "__main__":
    unittest.main()
