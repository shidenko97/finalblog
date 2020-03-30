from hashlib import md5

from bcrypt import checkpw, gensalt, hashpw
from flask_security import RoleMixin, UserMixin

from blog import db


# M2M links between Users and Roles
user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"))
)


class User(db.Model, UserMixin):
    """User model"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    fullname = db.Column(db.String(64))
    birthday = db.Column(db.Date)
    sex = db.Column(db.String(1))
    password = db.Column(db.String(64))
    active = db.Column(db.Boolean)
    roles = db.relationship("Role", secondary=user_role,
                            backref=db.backref("admin", lazy="dynamic"))

    def __repr__(self):
        return f"{self.fullname} [{self.email}]"

    def avatar(self, size: int = 120) -> str:
        """
        Function returns an avatar from gravatar service
        :param size: Size of image
        :type size: int
        :return: URL of avatar
        :rtype: str
        """

        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def hash_password(self):
        """Hash current password by bcrypt module"""

        password_hash = hashpw(self.password.encode("utf-8"), gensalt())
        self.password = password_hash.decode("utf-8")

    def verify_pass(self, password: str) -> bool:
        """
        Check if password is correct
        :param password: Password to check
        :type: str
        :return: Result of check
        :rtype: bool
        """

        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))


class Role(db.Model, RoleMixin):
    """User's roles"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(255))
