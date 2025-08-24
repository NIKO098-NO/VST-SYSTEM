from flask import Flask, render_template, request, redirect, url_for, session, flash
from itsdangerous import URLSafeSerializer
import hashlib, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET","dev_secret")
APP_SECRET = os.environ.get("APP_SECRET","dev_app_secret")
serializer = URLSafeSerializer(APP_SECRET)

users = {"ceo":{"password":"ceo123","role":"CEO"},
         "cfo":{"password":"cfo123","role":"CFO"},
         "guard":{"password":"guard123","role":"VST_GUARD"}}
staff = {}
logs = []

def create_staff_token(staff_id,name):
    payload={"staff_id":staff_id,"name":name,"timestamp":str(datetime.now())}
    return serializer.dumps(payload)

def verify_staff_token(token):
    try:
        data = serializer.loads(token)
        staff_id = data.get("staff_id")
        if staff_id in staff:
            return True,data
        else:
            return False,"Staff ID not registered"
    except:
        return False,"Invalid token"

def fingerprint_hash(file):
    content=file.read()
    file.seek(0)
    return hashlib.sha256(content).hexdigest()

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if username in users and users[username]["password"]==password:
            session["user"]=username
            session["role"]=users[username]["role"]
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html",user=session["user"],role=session["role"])

if __name__=="__main__":
    app.run(debug=True)
