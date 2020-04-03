from sqlalchemy import and_

from blog import db
from blog.auth.models import Role, User


def save_changes(obj: db.Model):
    """
    Add and commit changes to DB
    :param obj: Flask model
    :type obj: db.Model
    """

    db.session.add(obj)
    db.session.commit()


def get_all_users() -> list:
    """
    Get list of users
    :return: List of users
    :rtype: list
    """

    return User.query.order_by(User.id.asc()).all()


def create_user(data: dict) -> User:
    """
    Create a new user
    :param data: Fields of new record
    :type data: dict
    :return: Created user model
    :rtype: User
    :raise ValueError: If the email already exists.
    """

    if User.query.filter_by(email=data["email"]).first():
        raise ValueError("The email already exists")

    user = User(**data)
    user.active = True
    user.roles.append(Role.query.filter_by(name="User").first())
    user.hash_password()

    save_changes(obj=user)

    return user


def get_user(user_id: int) -> User:
    """
    Get specific user
    :param user_id: User's identifier
    :type user_id: int
    :return: Found user
    :rtype: User
    """

    return User.query.filter_by(id=user_id).one()


def delete_user(user_id: int):
    """
    Delete specific user
    :param user_id: User's identifier
    :type user_id: int
    """

    User.query.filter_by(id=user_id).delete()
    db.session.commit()


def change_user(user_id: int, data: dict) -> User:
    """
    Change specific user
    :param user_id: User's identifier
    :type user_id: int
    :param data: Fields of new record
    :type data: dict
    :return: Changed user model
    :rtype: User
    :raise ValueError: If the email already exists.
    """

    user = get_user(user_id)

    # Check if email exists in another profile
    if (User
            .query
            .filter(and_(User.email == data["email"], User.id != user_id))
            .first()):
        raise ValueError("The email already exists")

    user.email = data["email"]
    user.fullname = data["fullname"]
    user.birthday = data["birthday"]
    user.sex = data["sex"]
    user.password = data["password"]

    save_changes(obj=user)
    return user


def get_all_roles() -> list:
    """
    Get list of roles
    :return: List of roles
    :rtype: list
    """

    return Role.query.all()


def get_role(role_id: int) -> Role:
    """
    Get specific role
    :param role_id: Role's identifier
    :type role_id: int
    :return: Found role
    :rtype: Role
    """

    return Role.query.filter_by(id=role_id).one()
