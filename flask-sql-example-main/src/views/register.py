from flask import Blueprint, render_template

bp = Blueprint("register", __name__, url_prefix="/register")


@bp.route("", methods=["GET"])
def register():
    return render_template("register.html.jinja")

