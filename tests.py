import pytest

# Import tests from all modules
from blog.auth.tests import UserModelCase  # noqa: F401
from blog.post.tests import CommentModelCase, PostModelCase  # noqa: F401
from chat.tests.test_chat import *  # noqa: F401,F403


if __name__ == "__main__":
    pytest.main()
