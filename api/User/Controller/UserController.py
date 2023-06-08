import os

from flask import request, Blueprint, session

from Company.Model.Company import Company
from Project.Model.Project import Project
from Skill.Model.Skill import Skill
from utils.DataValidator import convert_string_to_date
from utils.SessionsUtils import build_response
from utils.TokenUtils import token_required
from User.Model.User import User
from Social.Model.Role import Role
from db import db
import json

user_app = Blueprint(
    "user",
    __name__,
    url_prefix="/api/users/")


@user_app.route("", methods=["GET"])
@token_required
def get_all_users():
    users = [str(user) for user in User.query.all()]

    return build_response(users, 200)


@user_app.route("<id>/", methods=["GET"])
@token_required
def get_user_page(id):
    user = db.get_or_404(User, id)

    return build_response(str(user), 200)


@user_app.route("", methods=["POST"])
def create_user():
    USER_ROLE_ID = db.session.execute(db.select(Role).where(Role.name == "User")).first().id

    user_role = db.get_or_404(Role, USER_ROLE_ID)
    error_messages = []

    form = json.loads(request.json)

    if db.session.execute(db.select(User).where(User.email == form["email"])).first():
        error_messages.append("User with this email already exists")
    elif form["password"] != form["confirm_password"]:
        error_messages.append("Passwords do not match")

    user = User(
                form["password"],
                form["email"],
                form["fio"],
                form["sex"],
                convert_string_to_date(form["date_of_birth"]),
                form["source_of_knowing_about_pskk"],
                form["phone_number"],
                form['role'] if form['role'] else user_role)

    # error_messages += validator.validate_user_data(user)

    if error_messages:
        return build_response(error_messages, 422)

    db.session.add(user)
    db.session.commit()

    return build_response("{" + f"'user_id': {user.id}" + "}", 201)


@user_app.route("<id>/", methods=["PUT"])
@token_required
def update_user(id):
    user = db.get_or_404(User, id)

    password = user.password
    form = json.loads(request.json)

    if "password" in form:
        if form["password"] != user.password:
            return build_response(["Incorrect password"], 422)

        if db.session.execute(db.select(User).where(User.password == form["new_password"])).first():
            return build_response(["User with this password already exists"], 422)

        if form["new_password"] != form["confirm_password"]:
            return build_response(["Passwords do not match"], 422)

        password = form["new_password"]

    projects_participated = [db.get_or_404(Project, project_id) for project_id in form['projects_participated']]
    projects_initiated = [db.get_or_404(Project, project_id) for project_id in form['projects_initiated']]

    companies = [db.get_or_404(Company, company_id) for company_id in form['companies']]
    superuser_in_companies = [db.get_or_404(Company, company_id) for company_id in form['superuser_in_companies']]

    skills = [db.get_or_404(Skill, skill_id) for skill_id in form['skills']]

    new_user = User(
                    password,
                    user.email,
                    form["fio"],
                    form["sex"],
                    convert_string_to_date(form["date_of_birth"]),
                    form["source_of_knowing_about_pskk"],
                    form["phone_number"],
                    user.role,
                    form["address"],
                    form["post_index"],
                    form["inn"],
                    form["occupation"],
                    form["company_name"],
                    form["about_me"],
                    companies=companies,
                    superuser_in_companies=superuser_in_companies,
                    skills=skills,
                    projects_participated=projects_participated,
                    projects_initiated=projects_initiated,
                    id=user.id,
                    created_at=user.created_at)

    error_messages = []  # validator.validate_user_data(new_user)

    if error_messages:
        return build_response(error_messages, 422)

    db.session.delete(user)
    db.session.add(new_user)
    db.session.commit()

    return build_response("{}", 200)


@user_app.route("<id>/", methods=["DELETE"])
@token_required
def delete_user(id):
    user = db.get_or_404(User, id)

    db.session.delete(user)
    db.session.commit()

    return build_response("{}", 200)
