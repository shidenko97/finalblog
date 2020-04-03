from flask_restplus import fields

from blog.api.post import post_api


comment_model = post_api.model("Comment", {
    "id": fields.Integer(readonly=True, description="Comment's ID", example=1),
    "user_id": fields.Integer(readonly=True, description="Comment's user",
                              example=1),
    "post_id": fields.Integer(readonly=True, description="Comment's post",
                              example=1),
    "body": fields.String(required=True, description="Comment's body",
                          example="Cool post!"),
    "datetime": fields.DateTime(readonly=True,
                                description="Comment's datetime",
                                example="2020-01-01T00:00:00.000000"),
    "likes": fields.Integer(description="Comment's likes count", readonly=True,
                            attribute=lambda x: x.likes_count(), example="0"),
    "dislikes": fields.Integer(description="Comment's dislikes count",
                               attribute=lambda x: x.dislikes_count(),
                               readonly=True, example="0"),
})

post_model = post_api.model("Post", {
    "id": fields.Integer(readonly=True, description="Post's ID", example=1),
    "user_id": fields.Integer(readonly=True, description="Post's user",
                              example=1),
    "title": fields.String(required=True, description="Post's title",
                           max_length=64, example="My first post"),
    "slug": fields.String(readonly=True, description="Post's slug",
                          example="my-first-post"),
    "body": fields.String(required=True, description="Post's body",
                          example="Hi, it's my first post!"),
    "created": fields.DateTime(readonly=True, description="Post's created",
                               example="2020-01-01T00:00:00.000000"),
    "likes": fields.Integer(description="Post's likes count", readonly=True,
                            attribute=lambda x: x.likes_count(), example="0"),
    "dislikes": fields.Integer(description="Post's dislikes count",
                               attribute=lambda x: x.dislikes_count(),
                               readonly=True, example="0"),
    "comments": fields.List(fields.Nested(comment_model),
                            readonly=True, description="Post's comments"),
})
