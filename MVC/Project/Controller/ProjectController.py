import os

from flask import Blueprint
from db import db
from MVC.Project.Model.Project import Project

project_app = Blueprint(
    "project",
    __name__,
    url_prefix="/projects",
    template_folder=os.path.abspath(os.getcwd()) + '/MVC/Project/View')


# not implemented
@project_app.route("/<id>", methods=["GET"])
def get_project_page(id):
    pass


# not implemented
@project_app.route("/create", methods=["GET", "POST"])
def create_project():
    pass


# not implemented
@project_app.route("/update/<id>", methods=["GET", "POST"])
def update_project(id):
    pass


# not implemented
@project_app.route("/delete/<id>", methods=["POST"])
def delete_project(id):
    pass
