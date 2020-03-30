from flask import Blueprint

from blog import login
from blog.auth.models import User


bp = Blueprint("auth", __name__)


@login.user_loader
def load_user(user_id: str) -> User:
    """
    Returns current user
    :param user_id: ID of user
    :type: str
    :return: User's model
    :rtype: User
    """

    return User.query.get(int(user_id))


from blog.auth import routes  # noqa: E402, F401
