import os

from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import json
from RequestUtils.RequestUtils import get_headers

user_app = Blueprint("user",
                     __name__,
                     url_prefix="/users/",
                     template_folder='../View')

api_path = "http://localhost:5000/api/users/"


@user_app.route("", methods=["GET"])
def show_all_users():
    data = requests.get(api_path).json()

    users = [json.loads(obj) for obj in data]

    return render_template('show_all_users.html', users=users)


@user_app.route("<id>/", methods=["GET"])
def show_user_by_id(id):
    data = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()

    return render_template("show_user.html", user=data)


@user_app.route("create/", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        data = request.form
        response = requests.post(api_path, json=data)
        if response.status_code == 201:
            user_id = response.json()['user_id']
            return redirect(url_for("user.show_user_by_id", id=user_id))
        
        return render_template("show_create_user.html", user=data, error="Invalid data")
    
    return render_template("show_create_user.html")


@user_app.route("<id>/edit/", methods=["GET", "POST"])
def update_user(id):
    user = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()
                      
    if request.method == "POST":
        data = request.form

        response = requests.put(api_path + f"{id}/", json=data, headers=get_headers(session['token']))
        if response.status_code == 200:
            return redirect(url_for("user.show_user_by_id", id=id))
        
        return render_template("show_update_user.html", user=data, error="Invalid data")
    
    return render_template("show_update_user.html", user=user)


@user_app.route("<id>/delete/", methods=["GET"])
def delete_user(id):
    response = requests.delete(api_path + f"{id}/", headers=get_headers(session['token']))
    
    if response.status_code == 200:
        return redirect(url_for("user.show_all_users"))
    
    return redirect(url_for("user.show_user_by_id", id=id))
