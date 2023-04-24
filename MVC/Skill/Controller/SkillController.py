import os

from flask import Blueprint
from db import db
from MVC.Skill.Model.Skill import Skill

skill_app = Blueprint(
    "skill",
    __name__,
    url_prefix="/skills",
    template_folder=os.path.abspath(os.getcwd()) + '/MVC/Skill/View')


# not implemented
@skill_app.route("/<id>", methods=["GET"])
def get_skill_page(id):
    pass


# not implemented
@skill_app.route("/create", methods=["GET", "POST"])
def create_skill():
    pass


# not implemented
@skill_app.route("/update/<id>", methods=["GET", "POST"])
def update_skill(id):
    pass


# not implemented
@skill_app.route("/delete/<id>", methods=["POST"])
def delete_skill(id):
    pass
