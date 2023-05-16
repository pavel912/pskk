import os

from flask import Blueprint, request
from api.Company.Model.Company import Company
from api.Project.Model.Project import Project
from api.Skill.Model.Skill import Skill
from api.User.Model.User import User
from db import db
from utils.DataValidator import convert_string_to_date
from utils.SessionsUtils import build_response

company_app = Blueprint(
    "company",
    __name__,
    url_prefix="/api/company")


@company_app.route("/", methods=["GET"])
def get_all_companies():
    companies = [str(company) for company in Company.query.all()]
    return build_response(companies, 200)


@company_app.route("/<id>", methods=["GET"])
def get_company_by_id(id):
    company = db.get_or_404(Company, id)

    return build_response(str(company), 200)


@company_app.route("/", methods=["POST"])
def create_company():
    company = Company(
        request.json["company_name"],
        request.json["email"],
        request.json["phone_number"],
        request.json["representative_fio"],
        request.json["superuser_id"],
        request.json["address"],
        request.json["post_index"],
        request.json["inn"],
        convert_string_to_date(request.json["registered_as_company_at"])
    )

    db.session.add(company)
    db.session.commit()

    return build_response(f"'Created company with id': {company.id}", 201)


@company_app.route("/<id>", methods=["PUT"])
def update_company(id):
    old_company = db.get_or_404(Company, id)

    projects = [db.get_or_404(Project, project_id) for project_id in request.json['projects']]
    users = [db.get_or_404(User, user_id) for user_id in request.json['users']]
    skills = [db.get_or_404(Skill, skill_id) for skill_id in request.json['required_skills']]

    company = Company(
        request.json["company_name"],
        request.json["email"],
        request.json["phone_number"],
        request.json["representative_fio"],
        request.json["superuser_id"],
        request.json["address"],
        request.json["post_index"],
        request.json["inn"],
        convert_string_to_date(request.json["registered_as_company_at"]),
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


@company_app.route("/<id>", methods=["DELETE"])
def delete_company(id):
    company = db.get_or_404(Company, id)

    db.session.add(company)
    db.session.commit()

    return build_response("{}", 200)
