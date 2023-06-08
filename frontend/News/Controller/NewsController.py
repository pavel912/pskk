import os

from flask import Blueprint, request, render_template, redirect, url_for, session
import requests
import json
from RequestUtils.RequestUtils import get_headers

news_app = Blueprint("news",
                     __name__,
                     url_prefix="/news/",
                     template_folder='../View')

api_path = "http://localhost:5000/api/news/"

@news_app.route("", methods=["GET"])
def show_all_news():
    print(session['token'])
    data = requests.get(api_path).json()

    news = [json.loads(obj) for obj in data]

    return render_template('show_all_news.html', news=news)


@news_app.route("<id>/", methods=["GET"])
def show_news_by_id(id):
    data = requests.get(api_path + f"{id}/").json()

    return render_template("show_news.html", news=data)


@news_app.route("create/", methods=["GET", "POST"])
def create_news():
    if request.method == "POST":
        data = json.dumps(request.form)
        response = requests.post(api_path, json=data, headers=get_headers(session['token']))
        if response.status_code == 201:
            return redirect(url_for("show_all_news"))
        
        return render_template("show_create_news.html", news=data, error="Invalid data")
    
    return render_template("show_create_news.html")


@news_app.route("<id>/edit/", methods=["GET", "POST"])
def update_news(id):
    news = requests.get(api_path + f"{id}/", headers=get_headers(session['token'])).json()
                      
    if request.method == "POST":
        data = json.dumps(request.form)

        response = requests.put(api_path + f"{id}/", json=data, headers=get_headers(session['token']))
        if response.status_code == 200:
            return redirect(url_for("show_news_by_id"))
        
        return render_template("show_update_news.html", news=data, error="Invalid data")
    
    return render_template("show_update_news.html", news=news)


@news_app.route("<id>/delete/", methods=["GET"])
def delete_news(id):
    response = requests.delete(api_path + f"{id}/", headers=get_headers(session['token']))
    
    if response.status_code == 200:
        return redirect(url_for("show_all_news"))
    
    return redirect(url_for("show_news_by_id"))
