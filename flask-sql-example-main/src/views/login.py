from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import select
from ..models import Register, db

bp = Blueprint("login", __name__, url_prefix="/login")


@bp.route("", methods=["GET"])
def login():
    return render_template("login.html.jinja")

@bp.route("", methods=["POST"])
def check_login():
    gmail = request.form.get("email")
    password = request.form.get("password")

    if not id or not gmail or not password:
        return "fail", 400
    
    Gmail = db.session.query(Register).filter(Register.gmail == gmail).first()
    Password = db.session.query(Register).filter(Register.password == password).first()

    print(Gmail)
    print(Password)
    
    return redirect (url_for("login.login"))
    
