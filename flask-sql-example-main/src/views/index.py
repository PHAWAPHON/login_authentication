from flask import Blueprint, render_template, request, url_for, redirect, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from ..models import Register, db
import hashlib

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("", methods=["GET"])
def index():
    return render_template("index.html.jinja")

@bp.route("", methods=["POST"])
def create_user():
    userName = request.form.get("userName", "")
    gmail = request.form.get("gmail", "")
    password = request.form.get("password", "")
    salt = "5gz"
    hash_password = password+salt
    hashed = hashlib.md5(hash_password.encode())
    print(hashed.hexdigest())
    
    print(userName)
    print(gmail)
    print(password)

    if not userName or not gmail or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    existing_user = db.session.execute(select(Register).filter_by(userName=userName)).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    user = Register()
    user.userName = userName
    user.gmail = gmail
    user.password = hashed.hexdigest()
    
    print(user.userName)
    print(user.gmail)
    print(user.password)
    
    db.session.add(user)
    try:
        db.session.commit()
        return redirect(url_for("login.login"))
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while creating the user'}), 400
