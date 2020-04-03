from flask_restplus import Namespace


user_api = Namespace("Users", description="Blog users", path="/user")


from blog.api.user import routes  # noqa: E402, F401
