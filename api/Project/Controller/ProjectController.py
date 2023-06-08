import os

from flask import Blueprint, request

from Company.Model.Company import Company
from Skill.Model.Skill import Skill
from User.Model.User import User
from db import db
from Project.Model.Project import Project
from utils.SessionsUtils import build_response
from utils.DataValidator import convert_string_to_date
from utils.TokenUtils import token_required
import json

project_app = Blueprint(
    "project",
    __name__,
    url_prefix="/api/projects/")


@project_app.route("", methods=["GET"])
@token_required
def get_all_projects():
    projects = [str(project) for project in Project.query.all()]
    return build_response(projects, 200)


@project_app.route("<id>/", methods=["GET"])
@token_required
def get_project_by_id(id):
    project = db.get_or_404(Project, id)
    return str(project)


@project_app.route("", methods=["POST"])
@token_required
def create_project():
    form = json.loads(request.json)
    
    project = Project(
        form["name"],
        form["user_initiator_id"],
        form["project_type"],
        form["description"],
        convert_string_to_date(form["end_plan"]),
        [form["user_initiator_id"]]
    )

    db.session.add(project)
    db.session.commit()

    return build_response(f"'Created project with id': {project.id}", 201)


@project_app.route("<id>/", methods=["PUT"])
@token_required
def update_project(id):
    old_project = db.get_or_404(Project, id)

    form = json.loads(request.json)

    companies = [db.get_or_404(Company, company_id) for company_id in form['companies']]
    users = [db.get_or_404(User, user_id) for user_id in form['users']]
    skills = [db.get_or_404(Skill, skill_id) for skill_id in form['required_skills']]

    project = Project(
        form["name"],
        form["user_initiator_id"],
        form["project_type"],
        form["description"],
        convert_string_to_date(form["end_plan"]),
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


@project_app.route("<id>/", methods=["DELETE"])
@token_required
def delete_project(id):
    project = db.get_or_404(Project, id)

    db.session.delete(project)
    db.session.commit()

    return build_response("{}", 200)
