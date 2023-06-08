import os

from db import db
from flask import request, session, Blueprint, current_app
from User.Model.User import User
from utils.SessionsUtils import build_response
import json
import jwt

login_app = Blueprint(
    "login",
    __name__,
    url_prefix="/api/auth/")


@login_app.route("login/", methods=["POST"])
def login():
    form = json.loads(request.json)
    user = db.session.execute(db.select(User).where(User.email == form["email"] and
                                                    User.password == form["password"])).scalar()
    if not user:
        return build_response(["Incorrect login or password"], 401)
    
    token = jwt.encode(
            {"user_id": user.id},
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
    )

    return build_response("{" + f"""
        "message": "Successfully fetched auth token",
        "token": "{token}",
        "user_id": {user.id}
    """ + "}", 200)
