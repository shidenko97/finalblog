from flask_wtf import FlaskForm
from wtforms import DateField, PasswordField, SelectField, StringField, \
    SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

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


class RestorePasswordForm(FlaskForm):
    """Public form for restoring password through email"""

    email = StringField("Email", validators=[DataRequired(), Email(),
                                             Length(max=64)])
    submit = SubmitField("Restore")


class ResetPasswordForm(FlaskForm):
    """Public form for resetting password after restoring"""

    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=6, max=64)])
    password_repeat = PasswordField("Repeat Password",
                                    validators=[DataRequired(),
                                                EqualTo("password")])
    submit = SubmitField("Reset")


class ProfileForm(FlaskForm):
    """Form for editing profile"""

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=64)
        ]
    )
    fullname = StringField("Fullname", validators=[DataRequired(),
                                                   Length(max=64)])
    birthday = DateField("Birthday", validators=[Optional()])
    sex = SelectField("Sex",
                      choices=[("", " - "), ("m", "Male"), ("f", "Female")],
                      validators=[Optional()])
    password = PasswordField("Password", validators=[Length(min=6, max=64),
                                                     Optional()])
    submit = SubmitField("Submit")
