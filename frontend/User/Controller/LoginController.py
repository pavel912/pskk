import os

from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import json

login_app = Blueprint("login",
                     __name__,
                     url_prefix="/login/",
                     template_folder='../View')

api_path = "http://localhost:5000/api/auth/"


@login_app.route("login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = json.dumps(request.form)
        response = requests.post(api_path + "login/", json=data)
        if response.status_code == 200:
            answer = response.json()
            user_id, token = answer['user_id'], answer['token']
            session['token'] = token
            return redirect(f"/users/{user_id}/")
        
        return render_template("show_login.html", error="Invalid data")
    
    return render_template("show_login.html")