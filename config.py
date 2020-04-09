import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Default project config"""

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

    # Mail configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT") or 25)
    MAIL_USE_TLS = bool(os.getenv("MAIL_USE_TLS") or False)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    # AIOHTTP Chat
    CHAT_PORT = os.getenv("CHAT_PORT")


class TestConfig(Config):
    """Config for tests"""

    # App configuration
    DEBUG = False
    TESTING = True
    SECRET_KEY = "secret-key-for-app-tests"
