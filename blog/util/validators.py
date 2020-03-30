from flask_wtf import FlaskForm
from wtforms import Field, validators

from blog import db


class Unique:
    """Unique value validator in specific model"""

    def __init__(
        self,
        model: db.Model,
        field: Field,
        message: str = "This element already exists."
    ) -> None:
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form: FlaskForm, field: Field) -> None:
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise validators.ValidationError(self.message)
