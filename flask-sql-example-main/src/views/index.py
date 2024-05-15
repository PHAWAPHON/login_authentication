from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import select
from ..models import Register, db

bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("", methods=["GET"])
def index():
    return render_template("index.html.jinja")

@bp.route("", methods=["POST"])
def create_user():
    userName = request.form.get("userName")
    gmail = request.form.get("email")
    password = request.form.get("password")

    if not id or not gmail or not password:
        return "fail", 400
    
    user = Register()
    user.userName = userName
    user.gmail = gmail
    user.password = password

    db.session.add(user)
    db.session.commit()

    return redirect (url_for("index.index"))