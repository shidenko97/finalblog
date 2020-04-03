from flask_restplus import fields

from blog.api.post.models import comment_model, post_model
from blog.api.user import user_api
from blog.api.util.frp_password_field import PasswordFormat


email_regex = r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"

role_model = user_api.model("Role", {
    "id": fields.Integer(readonly=True, description="Role's ID", example=1),
    "name": fields.String(readonly=True, description="Role's name",
                          max_length=64, example="God"),
    "description": fields.String(readonly=True, max_length=255,
                                 example="Just a god",
                                 description="Role's description"),
})

user_model = user_api.model("User", {
    "id": fields.Integer(readonly=True, description="User's ID", example=1),
    "email": fields.String(required=True, description="User's email",
                           pattern=email_regex, max_length=64,
                           example="marshall@gmail.com"),
    "fullname": fields.String(required=True, description="User's fullname",
                              max_length=64,
                              example="Marshall Bruce Mathers III"),
    "birthday": fields.Date(description="User's birthday",
                            example="1990-01-01"),
    "sex": fields.String(description="User's sex", enum=["m", "f"],
                         example="m"),
    "password": PasswordFormat(required=True, description="User's password",
                               example="TheRealSl1mShady"),
    "active": fields.Boolean(readonly=True, description="User's active sign",
                             default=True),
    "avatar": fields.String(description="User's avatar", readonly=True,
                            attribute=lambda x: x.avatar(100),
                            example="https://www.gravatar.com/avatar/"
                                    "e0d49368f68cc49767b1eb09a2e9c4ca?"
                                    "d=identicon&s=100"),
    "roles": fields.List(fields.Nested(role_model), readonly=True,
                         description="User's roles"),
    "posts": fields.List(fields.Nested(post_model), readonly=True,
                         description="User's posts"),
    "comments": fields.List(fields.Nested(comment_model), readonly=True,
                            description="User's comments"),
})
