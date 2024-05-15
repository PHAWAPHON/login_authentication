from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from sqlalchemy.exc import IntegrityError
from ..models import Register, db
import redis
import jwt
import random
import smtplib
from email.message import EmailMessage
import jwt

r = redis.Redis(host='localhost', port=6379, db=0)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login("misternarn@gmail.com", "vuse xmch fosd yaxs")

bp = Blueprint("login", __name__, url_prefix="/login")

def generateOTP():
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    OTP = "".join(random.choices(string, k=6))
    return OTP

@bp.route("", methods=["GET"])
def login():
    return render_template("login.html.jinja")

@bp.route("/auth", methods=["POST"])
def check_login():
    email = request.form.get("gmail")
    password = request.form.get("password")

    if not email or not password:
        return "Email and password are required", 400

    user = Register.query.filter_by(gmail=email, password=password).first()
    if not user:
        return "Incorrect email or password", 401

    otp = generateOTP()

    r.set(email, otp)

    from_mail = "misternarn@gmail.com"
    to_mail = email 

    msg = EmailMessage()
    msg["Subject"] = "OTP Verification"
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg.set_content("Your OTP is " + otp)

    server.send_message(msg)

    return render_template("login.html.jinja", otp_required=True, email=email)

@bp.route("/verify", methods=["POST"])
def verify_otp():
    email = request.form.get("gmail")
    otp = request.form.get("otp")
    print(email)
    
    if not email or not otp:
        return "Email and OTP are required", 400

    stored_otp = r.get(email)
    if not stored_otp or stored_otp.decode('utf-8') != otp:
        return "Invalid OTP", 401

    token = jwt.encode({'gmail': email}, otp, algorithm='HS256')
    session['token'] = token
    
    return redirect(url_for("login.login"))
