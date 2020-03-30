from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from blog import db
from blog.auth import bp
from blog.auth.forms import LoginForm, RegistrationForm
from blog.auth.models import User, Role


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Public login view"""

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.verify_pass(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        elif not user.active:
            flash("You're banned!")
            return redirect(url_for("auth.login"))

        login_user(user, remember=True)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template("auth/multi_form.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    """Public logout view"""

    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    """Public registration view"""

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.active = True
        user.roles.append(Role.query.filter_by(name="User").first())
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you're now a registered user!")
        return redirect(url_for("auth.login"))

    return render_template("auth/multi_form.html", title="Sign Up", form=form)
