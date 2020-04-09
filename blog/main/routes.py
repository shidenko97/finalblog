from flask import render_template, current_app

from blog.main import bp


@bp.route("/")
def index():
    """Main site page"""

    return render_template("main/index.html")


@bp.route("/chat")
def chat():
    """"""

    return render_template("main/chat.html",
                           chat_port=current_app.config["CHAT_PORT"])
