from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import select
from ..models import Register, db

bp = Blueprint("register", __name__, url_prefix="/register")


@bp.route("", methods=["GET"])
def index():
    return render_template("register.html.jinja")

