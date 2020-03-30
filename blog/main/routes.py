from flask import render_template

from blog.main import bp


@bp.route("/")
def index():
    """Main site page"""

    return render_template("main/index.html")
