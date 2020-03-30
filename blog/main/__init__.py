from flask import Blueprint


bp = Blueprint("main", __name__)


from blog.main import routes  # noqa: E402, F401
