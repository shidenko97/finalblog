from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_materialize import Material
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


# Initiate components
db = SQLAlchemy()
migrate = Migrate()
material = Material()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."
mail = Mail()


def create_app():
    """Function for creating application instance"""

    # Initiate app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setting up components for app
    db.init_app(app)
    migrate.init_app(app, db)
    material.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from blog.main import bp as main_bp
    app.register_blueprint(main_bp)

    from blog.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
