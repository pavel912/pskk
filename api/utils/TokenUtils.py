from User.Model.User import User
from functools import wraps
import jwt
from flask import request, current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split("'")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

        current_user = User.get(data["user_id"])

        if current_user is None:
            return {
            "message": "Invalid Authentication token!",
            "data": None,
            "error": "Unauthorized"
        }, 401

        return f(*args, **kwargs)

    return decorated


def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split("'")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

        current_user = User.get(data["user_id"])
        
        if current_user is None:
            return {
            "message": "Invalid Authentication token!",
            "data": None,
            "error": "Unauthorized"
        }, 401

        if current_user.role.name != 'Admin':
            return {
            "message": "Not enough provilleges!",
            "data": None,
            "error": "Unauthorized"
        }, 401
        
        return f(*args, **kwargs)

    return decorated