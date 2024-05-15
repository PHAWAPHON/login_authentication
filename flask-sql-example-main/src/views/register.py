from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import select
from ..models import Register, db

bp = Blueprint("register", __name__, url_prefix="/register")


@bp.route("", methods=["GET"])
def index():
    return render_template("register.html.jinja")

@bp.route("", methods=["POST"])
def create():
    userName = request.form.get("userName")
    gmail = request.form.get("email")
    password = request.form.get("password")

    if not id or not gmail or not password:
        return "fail", 400
    



    return redirect (url_for("register.register"))