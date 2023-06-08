import os

from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import json
from RequestUtils.RequestUtils import get_headers

project_app = Blueprint("project",
                     __name__,
                     url_prefix="/projects/",
                     template_folder='../View')

api_path = "http://localhost:5000/api/projects/"


@project_app.route("", methods=["GET"])
def show_all_projects():
    data = requests.get(api_path, headers=get_headers(session['token'])).json()

    projects = [json.loads(obj) for obj in data]

    return render_template('show_all_projects.html', projects=projects)


@project_app.route("<id>/", methods=["GET"])
def show_project_by_id(id):
    data = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()

    return render_template("show_project.html", project=data)


@project_app.route("create/", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        data = json.dumps(request.form)
        response = requests.post(api_path, json=data, headers=get_headers(session['token']))
        if response.status_code == 201:
            return redirect(url_for("show_all_projects"))
        
        return render_template("show_create_project.html", project=data, error="Invalid data")
    
    return render_template("show_create_project.html")


@project_app.route("<id>/edit/", methods=["GET", "POST"])
def update_project(id):
    project = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()
                      
    if request.method == "POST":
        data = json.dumps(request.form)

        response = requests.put(api_path + f"{id}/", json=data, headers=get_headers(session['token']))
        if response.status_code == 200:
            return redirect(url_for("show_project_by_id"))
        
        return render_template("show_update_project.html", project=data, error="Invalid data")
    
    return render_template("show_update_project.html", project=project)


@project_app.route("<id>/delete/", methods=["GET"])
def delete_project(id):
    response = requests.delete(api_path + f"{id}/", headers=get_headers(session['token']))
    
    if response.status_code == 200:
        return redirect(url_for("show_all_projects"))
    
    return redirect(url_for("show_project_by_id"))
