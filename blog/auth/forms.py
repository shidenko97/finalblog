from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from blog.auth.models import User
from blog.util.validators import Unique


class LoginForm(FlaskForm):
    """Public login form"""

    email = StringField("Email", validators=[DataRequired(), Email(),
                                             Length(max=64)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6, max=64)])
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    """Public registration form"""

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=64),
            Unique(User, User.email, "The user already registered")
        ]
    )
    fullname = StringField("Fullname", validators=[DataRequired(),
                                                   Length(max=64)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6, max=64)])
    password_repeat = PasswordField("Repeat password",
                                    validators=[DataRequired(),
                                                EqualTo("password")])
    submit = SubmitField("Sign In")
