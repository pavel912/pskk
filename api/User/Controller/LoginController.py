import os

from db import db
from flask import request, session, Blueprint
from api.User.Model.User import User
from utils.SessionsUtils import build_response

login_app = Blueprint(
    "login",
    __name__,
    url_prefix="/api/auth")


@login_app.route("/login", methods=["POST"])
def login():
    user = db.session.execute(db.select(User).where(User.email == request.json["email"] and
                                                    User.password == request.json["password"])).scalar()
    if not user:
        return build_response(["Incorrect login or password"], 401)

    session['user_id'] = user.id
    session['role'] = user.role.name
    return build_response({}, 200)


@login_app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id", None)
    return build_response({}, 200)
