import os

from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import json
from RequestUtils.RequestUtils import get_headers

skill_app = Blueprint("skill",
                     __name__,
                     url_prefix="/skills/",
                     template_folder='../View')

api_path = "http://localhost:5000/api/skills/"


@skill_app.route("", methods=["GET"])
def show_all_skills():
    data = requests.get(api_path, headers=get_headers(session['token'])).json()

    skills = [json.loads(obj) for obj in data]

    return render_template('show_all_skills.html', skills=skills)


@skill_app.route("<id>/", methods=["GET"])
def show_skill_by_id(id):
    data = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()

    return render_template("show_skill.html", skill=data)


@skill_app.route("create/", methods=["GET", "POST"])
def create_skill():
    if request.method == "POST":
        data = request.form
        response = requests.post(api_path, json=data, headers=get_headers(session['token']))
        if response.status_code == 201:
            return redirect(url_for("show_all_skills"))
        
        return render_template("show_create_skill.html", skill=data, error="Invalid data")
    
    return render_template("show_create_skill.html")


@skill_app.route("<id>/edit/", methods=["GET", "POST"])
def update_skill(id):
    skill = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()
                      
    if request.method == "POST":
        data = request.form

        response = requests.put(api_path + f"{id}/", json=data, headers=get_headers(session['token']))
        if response.status_code == 200:
            return redirect(url_for("show_skill_by_id"))
        
        return render_template("show_update_skill.html", skill=data, error="Invalid data")
    
    return render_template("show_update_skill.html", skill=skill)


@skill_app.route("<id>/delete/", methods=["GET"])
def delete_skill(id):
    response = requests.delete(api_path + f"{id}/", headers=get_headers(session['token']))
    
    if response.status_code == 200:
        return redirect(url_for("show_all_skills"))
    
    return redirect(url_for("show_skill_by_id"))
