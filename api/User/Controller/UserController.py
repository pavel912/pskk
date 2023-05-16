import os

from flask import request, Blueprint

from api.Company.Model.Company import Company
from api.Project.Model.Project import Project
from api.Skill.Model.Skill import Skill
from utils.DataValidator import convert_string_to_date
from utils.SessionsUtils import is_exists_user_session, build_response, is_admin
from api.User.Model.User import User
from api.Social.Model.Role import Role
from db import db

user_app = Blueprint(
    "user",
    __name__,
    url_prefix="/api/users")


@user_app.route("/", methods=["GET"])
def get_all_users():
    users = [str(user) for user in User.query.all()]

    return build_response(users, 200)


@user_app.route("/<id>", methods=["GET"])
def get_user_page(id):
    if not is_exists_user_session(id):
        return build_response("{}", 401)

    user = db.get_or_404(User, id)

    return build_response(str(user), 200)


@user_app.route("/", methods=["POST"])
def create_user():
    USER_ROLE_ID = db.session.execute(db.select(Role).where(Role.name == "User")).first().id

    user_role = db.get_or_404(Role, USER_ROLE_ID)
    error_messages = []

    if db.session.execute(db.select(User).where(User.email == request.json["email"])).first():
        error_messages.append("User with this email already exists")
    elif request.json["password"] != request.json["confirm_password"]:
        error_messages.append("Passwords do not match")

    user = User(
                request.json["password"],
                request.json["email"],
                request.json["fio"],
                request.json["sex"],
                convert_string_to_date(request.json["date_of_birth"]),
                request.json["source_of_knowing_about_pskk"],
                request.json["phone_number"],
                request.json['role'] if request.json['role'] else user_role)

    # error_messages += validator.validate_user_data(user)

    if error_messages:
        return build_response(error_messages, 422)

    db.session.add(user)
    db.session.commit()

    return build_response(f"'Created user with id': {user.id}", 201)


@user_app.route("/<id>", methods=["PUT"])
def update_user(id):
    user = db.get_or_404(User, id)

    if not is_exists_user_session(id) and not is_admin():
        return build_response("{}", 401)

    password = user.password

    if "password" in request.json:
        if request.json["password"] != user.password:
            return build_response(["Incorrect password"], 422)

        if db.session.execute(db.select(User).where(User.password == request.json["new_password"])).first():
            return build_response(["User with this password already exists"], 422)

        if request.json["new_password"] != request.json["confirm_password"]:
            return build_response(["Passwords do not match"], 422)

        password = request.json["new_password"]

    projects_participated = [db.get_or_404(Project, project_id) for project_id in request.json['projects_participated']]
    projects_initiated = [db.get_or_404(Project, project_id) for project_id in request.json['projects_initiated']]

    companies = [db.get_or_404(Company, company_id) for company_id in request.json['companies']]
    superuser_in_companies = [db.get_or_404(Company, company_id) for company_id in request.json['superuser_in_companies']]

    skills = [db.get_or_404(Skill, skill_id) for skill_id in request.json['skills']]

    new_user = User(
                    password,
                    user.email,
                    request.json["fio"],
                    request.json["sex"],
                    convert_string_to_date(request.json["date_of_birth"]),
                    request.json["source_of_knowing_about_pskk"],
                    request.json["phone_number"],
                    user.role,
                    request.json["address"],
                    request.json["post_index"],
                    request.json["inn"],
                    request.json["occupation"],
                    request.json["company_name"],
                    request.json["about_me"],
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


# not implemented
@user_app.route("/<id>", methods=["DELETE"])
def delete_user(id):
    user = db.get_or_404(User, id)

    if not is_exists_user_session(id) and not is_admin():
        return build_response("{}", 401)

    db.session.delete(user)
    db.session.commit()

    return build_response("{}", 200)
