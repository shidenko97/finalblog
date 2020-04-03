from flask import Blueprint
from flask_restplus import Api

from blog.api.post import post_api
from blog.api.user import user_api


# Create API module and register instance
bp = Blueprint("api", __name__)
api = Api(
    bp,
    version="1.0",
    title="Final blog REST API",
    description="Simple REST API for my final blog with Flask-RESTPlus package"
)

# Register api namespaces
api.add_namespace(user_api)
api.add_namespace(post_api)
