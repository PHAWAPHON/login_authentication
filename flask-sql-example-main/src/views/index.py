from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import select
from ..models import Register, db
import math, random
import smtplib
from email.message import EmailMessage
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("misternarn@gmail.com", "vuse xmch fosd yaxs")
bp = Blueprint("index", __name__, url_prefix="/")

def generateOTP() :
    
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]
 
    return OTP
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
    opt = generateOTP()

    from_mail = "misternarn@gmail.com"
    server.login(from_mail, "vuse xmch fosd yaxs")
    
    to_mail = "phetchuen_p@silpakorn.edu"

    msg = EmailMessage()
    msg['Subject'] = "OTP Verification"
    msg['from'] = from_mail
    msg['to'] = to_mail
    msg.set_content("Yoiur OTP is " + opt)

    server.send_message(msg)


    return redirect (url_for("index.index"))