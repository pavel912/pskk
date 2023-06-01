import os

from flask import Blueprint, request

from api.Company.Model.Company import Company
from api.Project.Model.Project import Project
from api.User.Model.User import User
from db import db
from api.Skill.Model.Skill import Skill
from utils.SessionsUtils import is_exists_user_session, build_response, is_admin
import requests
import json

skill_app = Blueprint(
    "skill",
    __name__,
    url_prefix="/api/skills")


@skill_app.route("/", methods=["GET"])
def get_skills():
    skills = [str(skill) for skill in Skill.query.all()]
    return build_response(skills, 200)


@skill_app.route("/<id>", methods=["GET"])
def get_skill_by_id(id):
    skill = db.get_or_404(Skill, id)

    return build_response(str(skill), 200)


@skill_app.route("/", methods=["POST"])
def create_skill():
    skill = Skill(
        request.json['name'],
        request.json['skill_type'],
        "Created",
        request.json['description']
    )

    db.session.add(skill)
    db.session.commit()

    req_body = {
        'request_type': 'create_skill',
        'entity_type': 'skill',
        'entity_id': skill.id
    }

    response = requests.post("http://localhost:5000", json=json.dumps(req_body))

    if response.status_code >= 300:
        return build_response(f"'Failed to create skill'", 422)

    return build_response(f"'Created skill with id': {skill.id}", 201)


@skill_app.route("/<id>", methods=["PUT"])
def update_skill(id):
    old_skill = db.get_or_404(Skill, id)

    users = [db.get_or_404(User, user_id) for user_id in request.json['users']]
    companies = [db.get_or_404(Company, company_id) for company_id in request.json['companies']]
    projects = [db.get_or_404(Project, project_id) for project_id in request.json['projects']]

    skill = Skill(
        request.json['name'],
        request.json['skill_type'],
        request.json['status'],
        request.json['description'],
        users,
        companies,
        projects,
        id=old_skill.id,
        created_at=old_skill.created_at
    )

    db.session.delete(old_skill)
    db.session.add(skill)
    db.session.commit()

    req_body = {
        'request_type': 'validation',
        'entity_type': 'skill',
        'entity_id': skill.id
    }

    response = requests.post("http://localhost:5000/api/requests", json=json.dumps(req_body))

    if response.status_code >= 300:
        return build_response(f"'Failed to update skill with id': {skill.id}", 422)

    return build_response("{}", 200)


@skill_app.route("/<id>", methods=["DELETE"])
def delete_skill(id):
    old_skill = db.get_or_404(Skill, id)

    db.session.delete(old_skill)
    db.session.commit()

    return build_response("{}", 200)
