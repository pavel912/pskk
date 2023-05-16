import os

from flask import Blueprint, request

from api.Company.Model.Company import Company
from api.Skill.Model.Skill import Skill
from api.User.Model.User import User
from db import db
from api.Project.Model.Project import Project
from utils.SessionsUtils import build_response
from utils.DataValidator import convert_string_to_date

project_app = Blueprint(
    "project",
    __name__,
    url_prefix="/api/projects")


@project_app.route("/", methods=["GET"])
def get_all_projects():
    projects = [str(project) for project in Project.query.all()]
    return build_response(projects, 200)


@project_app.route("/<id>", methods=["GET"])
def get_project_by_id(id):
    project = db.get_or_404(Project, id)
    return str(project)


@project_app.route("/", methods=["POST"])
def create_project():
    project = Project(
        request.json["name"],
        request.json["user_initiator_id"],
        request.json["project_type"],
        request.json["description"],
        convert_string_to_date(request.json["end_plan"]),
        [request.json["user_initiator_id"]]
    )

    db.session.add(project)
    db.session.commit()

    return build_response(f"'Created project with id': {project.id}", 201)


@project_app.route("/<id>", methods=["PUT"])
def update_project(id):
    old_project = db.get_or_404(Project, id)

    companies = [db.get_or_404(Company, company_id) for company_id in request.json['companies']]
    users = [db.get_or_404(User, user_id) for user_id in request.json['users']]
    skills = [db.get_or_404(Skill, skill_id) for skill_id in request.json['required_skills']]

    project = Project(
        request.json["name"],
        request.json["user_initiator_id"],
        request.json["project_type"],
        request.json["description"],
        convert_string_to_date(request.json["end_plan"]),
        users,
        companies,
        skills,
        id=old_project.id,
        created_at=old_project.created_at
    )

    db.session.delete(old_project)
    db.session.add(project)
    db.session.commit()

    return build_response("{}", 200)


@project_app.route("/<id>", methods=["DELETE"])
def delete_project(id):
    project = db.get_or_404(Project, id)

    db.session.delete(project)
    db.session.commit()

    return build_response("{}", 200)
