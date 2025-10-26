from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from core.db_config import db
from users.model import User

auth_bp = Blueprint("auth_bp", __name__)
reset_tokens = {}

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.form
    if User.query.filter((User.username==data['username']) | (User.email==data['email'])).first():
        flash("Username atau email sudah digunakan!", "error")
        return redirect(url_for("auth_bp.register_page"))

    hashed = generate_password_hash(data["password"])
    new_user = User(
        firstname=data["firstname"],
        lastname=data["lastname"],
        username=data["username"],
        email=data["email"],
        password=hashed
    )
    db.session.add(new_user)
    db.session.commit()
    flash("User berhasil didaftarkan, silakan login.", "success")
    return redirect(url_for("auth_bp.login_page"))

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.form
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        session['user_id'] = user.user_id
        session['username'] = user.username
        flash(f"Selamat datang, {user.firstname}!", "success")
        return redirect(url_for("auth_bp.dashboard_page"))
    else:
        flash("Username atau password salah!", "error")
        return redirect(url_for("auth_bp.login_page"))


@auth_bp.route("/dashboard")
def dashboard_page():
    if 'username' not in session:
        flash("Silakan login terlebih dahulu.", "error")
        return redirect(url_for('auth_bp.login_page'))
    
    return render_template("dashboard.html", username=session['username'])


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Berhasil logout.", "info")
    return render_template("logout.html")


@auth_bp.route("/")
def index_page():
    return render_template("index.html")

@auth_bp.route("/login")
def login_page():
    return render_template("login.html")

@auth_bp.route("/register")
def register_page():
    return render_template("register.html")

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password_page():
    if request.method == "POST":
        email = request.form.get("email")
        token = uuid4()
        reset_tokens[token] = email
        print(f"[INFO] Link reset untuk {email}: http://127.0.0.1:5000/reset-password/{token}")
        flash("Tautan reset telah dikirim ke terminal.", "info")
        return redirect(url_for("auth_bp.login_page"))
    return render_template("forgot_password.html")
