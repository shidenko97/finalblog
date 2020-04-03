from flask_httpauth import HTTPBasicAuth

from blog.auth.models import User


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    """
    Validate basic auth for API module
    :param username: User's name
    :type username: str
    :param password: User's password
    :type password: str
    :return: Result of validate
    :rtype: bool
    """

    user = User.query.filter_by(email=username).first()

    if user is None or not user.verify_pass(password):
        return False

    return True
