import os

from flask import Blueprint, request

from Company.Model.Company import Company
from Project.Model.Project import Project
from User.Model.User import User
from db import db
from Skill.Model.Skill import Skill
from utils.SessionsUtils import build_response
from utils.TokenUtils import token_required
import requests
import json

skill_app = Blueprint(
    "skill",
    __name__,
    url_prefix="/api/skills/")


@skill_app.route("", methods=["GET"])
@token_required
def get_skills():
    skills = [str(skill) for skill in Skill.query.all()]
    return build_response(skills, 200)


@skill_app.route("<id>/", methods=["GET"])
@token_required
def get_skill_by_id(id):
    skill = db.get_or_404(Skill, id)

    return build_response(str(skill), 200)


@skill_app.route("", methods=["POST"])
@token_required
def create_skill():
    form = json.loads(request.json)

    skill = Skill(
        form['name'],
        form['skill_type'],
        "Created",
        form['description']
    )

    db.session.add(skill)
    db.session.commit()

    req_body = {
        'request_type': 'validation',
        'entity_type': 'skill',
        'entity_id': skill.id
    }

    response = requests.post("http://localhost:5000/api/requests", json=json.dumps(req_body))

    if response.status_code >= 300:
        return build_response(f"'Failed to create skill'", 422)

    return build_response(f"'Created skill with id': {skill.id}", 201)


@skill_app.route("<id>/", methods=["PUT"])
@token_required
def update_skill(id):
    old_skill = db.get_or_404(Skill, id)

    form = json.loads(request.json)

    users = [db.get_or_404(User, user_id) for user_id in form['users']]
    companies = [db.get_or_404(Company, company_id) for company_id in form['companies']]
    projects = [db.get_or_404(Project, project_id) for project_id in form['projects']]

    skill = Skill(
        form['name'],
        form['skill_type'],
        form['status'],
        form['description'],
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


@skill_app.route("<id>/", methods=["DELETE"])
@token_required
def delete_skill(id):
    old_skill = db.get_or_404(Skill, id)

    db.session.delete(old_skill)
    db.session.commit()

    return build_response("{}", 200)
