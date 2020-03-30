import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """"""

    # App configuration
    DEBUG = bool(os.getenv("DEBUG") or False)
    SECRET_KEY = os.getenv("SECRET_KEY") or "my-super-secret-key"

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = (os.getenv("DATABASE_URI") or
                               "sqlite:///" + os.path.join(basedir, "blog.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Login configuration
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT") or "123456789"
    SECURITY_PASSWORD_HASH = os.getenv("SECURITY_PASSWORD_HASH") or "bcrypt"
