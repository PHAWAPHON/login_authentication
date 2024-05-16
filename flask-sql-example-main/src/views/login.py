from flask import Blueprint, render_template, request, url_for, redirect, session, flash, jsonify
import flask
from sqlalchemy.exc import IntegrityError
from sqlalchemy import  update, select
from ..models import Register, db
import redis, jwt, random, smtplib, hashlib
from email.message import EmailMessage 

r = redis.Redis(host='localhost', port=6379, db=0)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("", "")

bp = Blueprint("login", __name__, url_prefix="/login")

def generateOTP():
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTP = "".join(random.choices(string, k=6))
    return OTP

@bp.route("", methods=["GET"])
def login():
    return render_template("login.html.jinja")

@bp.route("", methods=["POST"])
def check_login():
    email = request.form.get("gmail")
    password = request.form.get("password")

    if not email or not password:
        return "Email and password are required", 400
    
    user = Register.query.filter_by(gmail=email).first()
    
    #print(user.password)
    #print(hashlib.md5((password + "5gz").encode()).hexdigest())
    
    if not user or user.password != hashlib.md5((password + "5gz").encode()).hexdigest():
        return "Incorrect email or password", 401
    
    
    otp = generateOTP()
    r.set(email, otp)

    from_mail = ""
    to_mail = email 

    msg = EmailMessage()
    msg["Subject"] = "OTP Verification"
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg.set_content("Your OTP is " + otp)
    r.expire(email, 60)
    server.send_message(msg)

    return render_template("login.html.jinja", otp_required=True, email=email)


@bp.route("/verify", methods=["POST"])
def verify_otp():
    email = request.form.get("email")
    otp = request.form.get("otp")
    print(email)
    
    if not email or not otp:
        return "Email and OTP are required", 400

    stored_otp = r.get(email)
    if not stored_otp or stored_otp.decode('utf-8') != otp:
        return "Invalid OTP", 401
    
    secret_key = "LOL"

    token = jwt.encode({'gmail': email}, secret_key , algorithm='HS256')

    db.session.execute(update(Register).where(Register.gmail == email).values({"token":token}))
    db.session.commit()
    
    print(token)
    return redirect(url_for("login.login"))

@bp.route("/push_token", methods=["GET"])
def push_token():
    headers = flask.request.headers
    bearer = headers.get('Authorization')

    if not bearer or 'Bearer ' not in bearer:
        return jsonify({"error": "Invalid token"}), 401

    token = bearer.split()[1]
    user = Register.query.filter_by(token=token).first()

    if not user:
        return jsonify({"error": "User not found or token is invalid"}), 401
    else:
        
        return jsonify({"email": user.gmail,"status": "success"}), 200
    
    
    

    

