from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from blog import db
from blog.post import bp
from blog.post.forms import CommentForm, PostForm
from blog.post.models import Comment, Post


@bp.route("/")
@login_required
def all_posts():
    """Show all posts"""

    # Page for pagination
    page = request.args.get("page", 1, type=int)
    # Posts with pagination
    posts = Post.query.order_by(Post.created.desc()).paginate(
        page, Post.POSTS_PER_PAGE, False
    )
    # Buttons for pagination
    next_url = url_for("post.all_posts", page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for("post.all_posts", page=posts.prev_num) \
        if posts.has_prev else None

    return render_template("post/index.html", posts=posts.items,
                           next_page=next_url, prev_page=prev_url,
                           current_page=page)


@bp.route("/<string:slug>", methods=["GET", "POST"])
@login_required
def view_post(slug: str):
    """Show post by slug"""

    post = Post.query.filter_by(slug=slug).first_or_404()

    form = CommentForm()

    if request.method == "POST" and form.validate_on_submit():
        comment = Comment()
        comment.body = form.body.data
        comment.user_id = current_user.id
        comment.post_id = post.id
        db.session.add(comment)
        db.session.commit()
        flash("You're successfully create the comment")
        return redirect(url_for("post.view_post", slug=slug))

    return render_template("post/view.html", post=post, comment_form=form)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    """Create post"""

    form = PostForm()

    if request.method == "POST" and form.validate_on_submit():
        post = Post()
        form.populate_obj(post)
        post.user_id = current_user.id
        post.generate_slug()
        db.session.add(post)
        db.session.commit()
        flash("You're successfully create the post")
        return redirect(url_for("post.view_post", slug=post.slug))

    return render_template("post/form.html", form=form,
                           title="Create a new post")


@bp.route("/<string:slug>/edit", methods=["GET", "POST"])
@login_required
def edit_post(slug: str):
    """Edit post"""

    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm(obj=post)

    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(post)
        post.generate_slug()
        db.session.add(post)
        db.session.commit()
        flash("You're successfully edit the post")
        return redirect(url_for("post.view_post", slug=post.slug))

    return render_template("post/form.html", form=form,
                           title="Edit a post")


@bp.route("/<string:slug>/delete")
@login_required
def delete_post(slug: str):
    """Delete post"""

    post = Post.query.filter_by(slug=slug).first_or_404()
    db.session.delete(post)
    db.session.commit()
    flash("You're successfully delete the post")

    return redirect(url_for("post.all_posts"))


@bp.route("/<string:slug>/like")
@login_required
def like_post(slug: str):
    """Like post"""

    post = Post.query.filter_by(slug=slug).first_or_404()

    if not post.like(current_user.id):
        flash("You have unlike the post!")
    else:
        flash("You have like the post!")

    return redirect(url_for("post.view_post", slug=slug))


@bp.route("/<string:slug>/dislike")
@login_required
def dislike_post(slug: str):
    """Dislike post"""

    post = Post.query.filter_by(slug=slug).first_or_404()

    if not post.dislike(current_user.id):
        flash("You have undislike the post!")
    else:
        flash("You have dislike the post!")

    return redirect(url_for("post.view_post", slug=slug))


@bp.route("/<string:slug>/like/<int:comment_id>/like-comment")
@login_required
def like_comment(slug: str, comment_id: int):
    """Like comment"""

    comment = Comment.query.get_or_404(comment_id)

    if not comment.like(current_user.id):
        flash("You have unlike the comment!")
    else:
        flash("You have like the comment!")

    return redirect(url_for("post.view_post", slug=slug))


@bp.route("/<string:slug>/like/<int:comment_id>/dislike-comment")
@login_required
def dislike_comment(slug: str, comment_id: int):
    """Dislike comment"""

    comment = Comment.query.get_or_404(comment_id)

    if not comment.dislike(current_user.id):
        flash("You have undislike the comment!")
    else:
        flash("You have dislike the comment!")

    return redirect(url_for("post.view_post", slug=slug))
