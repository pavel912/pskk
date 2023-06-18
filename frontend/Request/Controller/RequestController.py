import json

import requests
from RequestUtils.RequestUtils import get_headers
from flask import Blueprint, request, render_template, redirect, url_for, session

request_app = Blueprint("request",
                     __name__,
                     url_prefix="/requests/",
                     template_folder='../View')

api_path = "http://localhost:5000/api/requests/"


@request_app.route("", methods=["GET"])
def show_all_requests():
    data = requests.get(api_path, headers=get_headers(session['token'])).json()

    reqs = [json.loads(obj) for obj in data]

    return render_template('show_all_requests.html', requests=reqs)


@request_app.route("<id>/", methods=["GET"])
def show_request_by_id(id):
    data = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()

    return render_template("show_request.html", request=data)


@request_app.route("<id>/edit/", methods=["GET", "POST"])
def update_request(id):
    req = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()
                      
    if request.method == "POST":
        data = request.form

        response = requests.put(api_path + f"{id}/", json=data, headers=get_headers(session['token']))
        if response.status_code == 200:
            return redirect(url_for("show_request_by_id"))
        
        return render_template("show_update_request.html", request=data, error="Invalid data")
    
    return render_template("show_update_request.html", request=req)


@request_app.route("<id>/delete/", methods=["GET"])
def delete_request(id):
    response = requests.delete(api_path + f"{id}/", headers=get_headers(session['token']))
    
    if response.status_code == 200:
        return redirect(url_for("show_all_requests"))
    
    return redirect(url_for("show_request_by_id"))
