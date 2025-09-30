from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.user_model import UserModel

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = UserModel.find_by_email(email)
        if user and UserModel.check_password(user["password"], password):
            session["user_id"] = user["id"]
            session["nama"] = user["nama"]
            # redirect ke dashboard dosen
            return redirect(url_for("kuesioner.dashboard"))
        else:
            flash("Email atau password salah")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        UserModel.create_user(nama, email, password)
        flash("Registrasi berhasil, silakan login")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
