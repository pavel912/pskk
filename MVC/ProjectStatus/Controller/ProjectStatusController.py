import os

from flask import Blueprint
from db import db
from MVC.ProjectStatus.Model.ProjectStatus import ProjectStatus

project_status_app = Blueprint(
    "project_status",
    __name__,
    url_prefix="/project_status",
    template_folder=os.path.abspath(os.getcwd()) + '/MVC/ProjectStatus/View')


# project status
# not implemented
@project_status_app.route("/<id>", methods=["GET"])
def get_project_status_page(id):
    pass


# not implemented
@project_status_app.route("/create", methods=["GET", "POST"])
def create_project_status():
    pass


# not implemented
@project_status_app.route("/update/<id>", methods=["GET", "POST"])
def update_project_status(id):
    pass


# not implemented
@project_status_app.route("/delete/<id>", methods=["POST"])
def delete_project_status(id):
    pass