from flask import abort, request
from flask_restplus import Resource
from sqlalchemy.orm.exc import NoResultFound

from blog.api.auth import auth
from blog.api.post import post_api
from blog.api.post.models import comment_model, post_model
from blog.api.post.utils import (change_post, comment_post, create_post,
                                 delete_post, dislike_comment, dislike_post,
                                 get_all_posts, get_post, like_comment,
                                 like_post)


@post_api.route("/")
class PostList(Resource):
    """Actions with not specific post"""

    # Basic auth required for those actions
    decorators = [auth.login_required]

    @post_api.doc("post_list")
    @post_api.marshal_list_with(post_model, envelope="data")
    def get(self):
        """Get list of all posts"""

        return get_all_posts()

    @post_api.expect(post_model, validate=True)
    @post_api.marshal_with(post_model, code=201)
    @post_api.doc("create_post", responses={
        201: "Success",
        400: "Validation Error"
    })
    def post(self):
        """Create a new post"""

        return create_post(request.json), 201


@post_api.route("/<string:slug>")
@post_api.response(404, "Post not found")
@post_api.param("slug", "The post slug")
class Post(Resource):
    """Actions with specific post"""

    # Basic auth required for those actions
    decorators = [auth.login_required]

    @post_api.doc("get_post", responses={
        200: "Success",
    })
    @post_api.marshal_with(post_model)
    def get(self, slug):
        """Get post by slug"""

        try:
            return get_post(slug)
        except NoResultFound:
            return abort(404, "Post not found")

    @post_api.doc("delete_post")
    @post_api.response(204, "Post deleted")
    def delete(self, slug):
        """Delete post by slug"""

        delete_post(slug)
        return "", 204

    @post_api.expect(post_model, validate=True)
    @post_api.marshal_with(post_model)
    def put(self, slug):
        """Change post by slug"""

        data = request.json

        try:
            return change_post(slug, data)
        except NoResultFound:
            return abort(404, "Post not found")


@post_api.route("/<string:slug>/like")
@post_api.response(404, "Post not found")
@post_api.param("slug", "The post slug")
class PostLike(Resource):
    """Like a specific post"""

    @post_api.doc("like_post", responses={
        200: "Success",
    })
    @post_api.marshal_with(post_model)
    def get(self, slug):
        """Like a specific post"""

        try:
            return like_post(slug)
        except NoResultFound:
            return abort(404, "Post not found")


@post_api.route("/<string:slug>/dislike")
@post_api.response(404, "Post not found")
@post_api.param("slug", "The post slug")
class PostDislike(Resource):
    """Dislike a specific post"""

    @post_api.doc("dislike_post", responses={
        200: "Success",
    })
    @post_api.marshal_with(post_model)
    def get(self, slug):
        """Dislike a specific post"""

        try:
            return dislike_post(slug)
        except NoResultFound:
            return abort(404, "Post not found")


@post_api.route("/<string:slug>/comment")
@post_api.response(404, "Post not found")
@post_api.param("slug", "The post slug")
class PostComment(Resource):
    """Comment a specific post"""

    @post_api.expect(comment_model, validate=True)
    @post_api.marshal_with(post_model, code=201)
    @post_api.doc("comment_post", responses={
        201: "Success",
        400: "Validation Error"
    })
    def post(self, slug):
        """Comment a specific post"""

        try:
            return comment_post(slug, request.json), 201
        except NoResultFound:
            return abort(404, "Post not found")


@post_api.route("/comment/<int:comment_id>/like")
@post_api.response(404, "Comment not found")
@post_api.param("comment_id", "The comment identifier")
class CommentLike(Resource):
    """Like a specific comment"""

    @post_api.doc("like_comment", responses={
        200: "Success",
    })
    @post_api.marshal_with(comment_model)
    def get(self, comment_id):
        """Like a specific comment"""

        try:
            return like_comment(comment_id)
        except NoResultFound:
            return abort(404, "Comment not found")


@post_api.route("/comment/<int:comment_id>/dislike")
@post_api.response(404, "Comment not found")
@post_api.param("comment_id", "The comment identifier")
class CommentDislike(Resource):
    """Dislike a specific comment"""

    @post_api.doc("dislike_comment", responses={
        200: "Success",
    })
    @post_api.marshal_with(comment_model)
    def get(self, comment_id):
        """Dislike a specific comment"""

        try:
            return dislike_comment(comment_id)
        except NoResultFound:
            return abort(404, "Comment not found")
