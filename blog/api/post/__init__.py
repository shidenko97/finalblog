from flask_restplus import Namespace


post_api = Namespace("Posts", description="Blog posts", path="/post")


from blog.api.post import routes  # noqa: E402, F401
