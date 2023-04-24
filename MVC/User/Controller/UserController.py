import os

from flask import render_template, request, redirect, make_response, Blueprint
from db import db
from utils.DataValidator import convert_string_to_date
from utils.SessionsUtils import is_exists_user_session
from MVC.User.Model.User import User

user_app = Blueprint(
    "user",
    __name__,
    url_prefix="/users",
    template_folder=os.path.abspath(os.getcwd()) + '/MVC/User/View')


@user_app.route("/", methods=["GET"])
def get_all_users():
    users = db.session.query(User).get()

    return users


@user_app.route("/<id>", methods=["GET"])
def get_user_page(id):
    if not is_exists_user_session(id):
        return redirect("/auth/login")

    user = db.get_or_404(User, id)

    return render_template('userpage.html', user=user)


@user_app.route("/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        error_messages = []

        if db.session.execute(db.select(User).where(User.email == request.form["email"])).first():
            error_messages.append("User with this email already exists")
        elif request.form["password"] != request.form["confirm_password"]:
            error_messages.append("Passwords do not match")

        user = User(
                    request.form["password"],
                    request.form["email"],
                    request.form["fio"],
                    request.form["sex"],
                    convert_string_to_date(request.form["date_of_birth"]),
                    request.form["source_of_knowing_about_pskk"],
                    request.form["phone_number"])

        # error_messages += validator.validate_user_data(user)

        if error_messages:
            return make_response(render_template('create_user_account.html',
                                                 error_messages=error_messages,
                                                 user=user),
                                 401)

        db.session.add(user)
        db.session.commit()
        return redirect("/auth/login")

    return render_template('create_user_account.html')


@user_app.route("update/<id>", methods=["GET", "POST"])
def update_user(id):
    if not is_exists_user_session(id):
        return redirect("/auth/login")

    user = db.get_or_404(User, id)

    if request.method == "POST":

        password = user.password

        if request.form["password"]:
            if request.form["password"] != user.password:
                return make_response(render_template('update_userdata.html',
                                                     error_messages=["Incorrect password"],
                                                     user=user),
                                     401)

            if db.session.execute(db.select(User).where(User.password == request.form["new_password"])).first():
                return make_response(render_template('update_userdata.html',
                                                     error_messages=["User with this password already exists"],
                                                     user=user),
                                     401)
            if request.form["new_password"] != request.form["confirm_password"]:
                return make_response(render_template('update_userdata.html',
                                                     error_messages=["Passwords do not match"],
                                                     user=user),
                                     401)

            password = request.form["new_password"]

        new_user = User(
                        password,
                        user.email,
                        request.form["fio"],
                        request.form["sex"],
                        convert_string_to_date(request.form["date_of_birth"]),
                        request.form["source_of_knowing_about_pskk"],
                        request.form["phone_number"],
                        request.form["address"],
                        request.form["post_index"],
                        request.form["inn"],
                        request.form["occupation"],
                        request.form["company_name"],
                        request.form["about_me"],
                        companies=user.companies,
                        superuser_in_companies=user.superuser_in_companies,
                        skills=user.skills,
                        projects_participated=user.projects_participated,
                        projects_initiated=user.projects_initiated,
                        id=user.id,
                        created_at=user.created_at)

        error_messages = []  # validator.validate_user_data(new_user)

        if error_messages:
            return make_response(render_template('update_userdata.html',
                                                 error_messages=error_messages,
                                                 user=user),
                                 401)

        db.session.delete(user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(f"/users/{user.id}")

    return render_template('update_userdata.html', user=user)


# not implemented
@user_app.route("/delete/<id>", methods=["POST"])
def delete_user(id):
    pass