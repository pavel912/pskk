import os

from db import db
from flask import render_template, request, redirect, make_response, session, Blueprint
from MVC.User.Model.User import User

login_app = Blueprint(
    "login",
    __name__,
    url_prefix="/auth",
    template_folder=os.path.abspath(os.getcwd()) + '/MVC/User/View')


@login_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.username == request.form["username"] and
                                                        User.password == request.form["password"])).scalar()
        if not user:
            return make_response(render_template('login.html', flash_message="Incorrect login or password"), 401)

        session['user_id'] = user.id
        return redirect(f"/users/{user.id}")

    return render_template('login.html')


@login_app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return redirect("/auth/login")
