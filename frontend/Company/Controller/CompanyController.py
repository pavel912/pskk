import os

from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import json
from RequestUtils.RequestUtils import get_headers

company_app = Blueprint("company",
                     __name__,
                     url_prefix="/company/",
                     template_folder='../View')

api_path = "http://localhost:5000/api/company/"


@company_app.route("", methods=["GET"])
def show_all_companies():
    data = requests.get(api_path, headers=get_headers(session['token'])).json()

    companies = [json.loads(obj) for obj in data]

    return render_template('show_all_companies.html', companies=companies)


@company_app.route("<id>/", methods=["GET"])
def show_company_by_id(id):
    data = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()

    return render_template("show_company.html", company=data)


@company_app.route("create/", methods=["GET", "POST"])
def create_company():
    if request.method == "POST":
        data = json.dumps(request.form)
        response = requests.post(api_path, json=data, headers=get_headers(session['token']))
        if response.status_code == 201:
            return redirect(url_for("show_all_companies"))
        
        return render_template("show_create_company.html", company=data, error="Invalid data")
    
    return render_template("show_create_company.html")


@company_app.route("<id>/edit/", methods=["GET", "POST"])
def update_company(id):
    company = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()
                      
    if request.method == "POST":
        data = json.dumps(request.form)

        response = requests.put(api_path + f"{id}/", json=data, headers=get_headers(session['token']))
        if response.status_code == 200:
            return redirect(url_for("show_company_by_id"))
        
        return render_template("show_update_company.html", company=data, error="Invalid data")
    
    return render_template("show_update_company.html", company=company)


@company_app.route("<id>/delete/", methods=["GET"])
def delete_company(id):
    response = requests.delete(api_path + f"{id}/", headers=get_headers(session['token']))
    
    if response.status_code == 200:
        return redirect(url_for("show_all_companies"))
    
    return redirect(url_for("show_company_by_id"))
