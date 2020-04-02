from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    """Form for creating comment"""

    body = StringField("Comment", validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Send")


class PostForm(FlaskForm):
    """Form for creating/editing post"""

    title = StringField("Title", validators=[DataRequired(), Length(max=64)])
    body = StringField("Body", validators=[DataRequired()])
    submit = SubmitField("Send")
