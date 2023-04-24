import os

from flask import Blueprint
from MVC.Company.Model.Company import Company
from db import db

company_app = Blueprint(
    "company",
    __name__,
    url_prefix="/company",
    template_folder=os.path.abspath(os.getcwd()) + '/MVC/Company/View')


# not implemented
@company_app.route("/<id>", methods=["GET"])
def get_company_page(id):
    pass


# not implemented
@company_app.route("/create", methods=["GET", "POST"])
def create_company():
    pass


# not implemented
@company_app.route("/update/<id>", methods=["GET", "POST"])
def update_company(id):
    pass


# not implemented
@company_app.route("/delete/<id>", methods=["POST"])
def delete_company(id):
    pass