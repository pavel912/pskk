import os

from flask import Blueprint
from db import db
from MVC.Request.Model.Request import Request

request_app = Blueprint(
    "request",
    __name__,
    url_prefix="/requests",
    template_folder=os.path.abspath(os.getcwd()) + '/MVC/Request/View')


# not implemented
@request_app.route("/<id>", methods=["GET"])
def get_request_page(id):
    pass


# not implemented
@request_app.route("/create", methods=["GET", "POST"])
def create_request():
    pass


# not implemented
@request_app.route("/update/<id>", methods=["GET", "POST"])
def update_request(id):
    pass


# not implemented
@request_app.route("/delete/<id>", methods=["POST"])
def delete_request(id):
    pass
