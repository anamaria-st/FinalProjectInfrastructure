from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return redirect(url_for("main.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Lógica de ejemplo: usuario / password fijos
        if username == "admin" and password == "secret":
            return render_template("login.html", success=True)
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)
