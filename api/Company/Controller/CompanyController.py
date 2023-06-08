import json
import os

from flask import Blueprint, request
from Company.Model.Company import Company
from Project.Model.Project import Project
from Skill.Model.Skill import Skill
from User.Model.User import User
from db import db
from utils.DataValidator import convert_string_to_date
from utils.SessionsUtils import build_response
from utils.TokenUtils import token_required

company_app = Blueprint(
    "company",
    __name__,
    url_prefix="/api/company/")


@company_app.route("", methods=["GET"])
@token_required
def get_all_companies():
    companies = [str(company) for company in Company.query.all()]
    return build_response(companies, 200)


@company_app.route("<id>/", methods=["GET"])
@token_required
def get_company_by_id(id):
    company = db.get_or_404(Company, id)

    return build_response(str(company), 200)


@company_app.route("", methods=["POST"])
@token_required
def create_company():
    form = json.loads(request.json)
    
    company = Company(
        form["company_name"],
        form["email"],
        form["phone_number"],
        form["representative_fio"],
        form["superuser_id"],
        form["address"],
        form["post_index"],
        form["inn"],
        convert_string_to_date(form["registered_as_company_at"])
    )

    db.session.add(company)
    db.session.commit()

    return build_response(f"'Created company with id': {company.id}", 201)


@company_app.route("<id>/", methods=["PUT"])
@token_required
def update_company(id):
    old_company = db.get_or_404(Company, id)

    form = json.loads(request.json)

    projects = [db.get_or_404(Project, project_id) for project_id in form['projects']]
    users = [db.get_or_404(User, user_id) for user_id in form['users']]
    skills = [db.get_or_404(Skill, skill_id) for skill_id in form['required_skills']]

    company = Company(
        form["company_name"],
        form["email"],
        form["phone_number"],
        form["representative_fio"],
        form["superuser_id"],
        form["address"],
        form["post_index"],
        form["inn"],
        convert_string_to_date(form["registered_as_company_at"]),
        users,
        skills,
        projects,
        id=old_company.id,
        created_at=old_company.created_at
    )

    db.session.delete(old_company)
    db.session.add(company)
    db.session.commit()

    return build_response("{}", 200)


@company_app.route("<id>/", methods=["DELETE"])
@token_required
def delete_company(id):
    company = db.get_or_404(Company, id)

    db.session.add(company)
    db.session.commit()

    return build_response("{}", 200)
