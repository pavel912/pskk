from flask import render_template, request, redirect, make_response, session
from entities.News import News
from entities.User import User
from entities.Project import Project
from entities.Company import Company
from entities.ProjectStatus import ProjectStatus
from entities.Skill import Skill
from utils.Data_Validator import Data_Validator
from app_db import app, db

validator = Data_Validator()

with app.app_context():
    db.drop_all()
    db.create_all()

    # add test data
    news1 = News("Foo bar", "Foo bar")
    news2 = News("Fuzz buzz", "Fuzz buzz")
    user = User("plobanov", "plobanov", "", "", "", validator.convert_string_to_date(""), "", "")
    db.session.add(news1)
    db.session.add(news2)
    db.session.add(user)
    db.session.commit()


# main page
@app.route('/', methods=["GET"])
def index():
    news = db.session.execute(db.select(News).order_by(News.created_at.desc()).limit(3)).scalars()
    return render_template('index.html', news=news, bigheader=True)


# news
@app.route('/news/<id>/', methods=["GET"])
def get_news_page(id):
    news = db.get_or_404(News, int(id))
    return render_template('news.html', news=news)


# not implemented
@app.route('/news/create', methods=["GET", "POST"])
def create_news():
    pass


# not implemented
@app.route('/news/<id>/update', methods=["GET", "POST"])
def update_news(id):
    pass


# not implemented
@app.route('/news/<id>/delete', methods=["POST"])
def delete_news(id):
    pass


# login
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = db.session.execute(db.select(User).where(User.username == request.form["username"] and
                                                        User.password == request.form["password"])).scalar()
        if not user:
            return make_response(render_template('login.html', flash_message="Incorrect login or password"), 401)

        session['user_id'] = user.id
        return redirect(f"/user/id/{user.id}")

    return render_template('login.html')


@app.route('/logout', methods=["GET"])
def logout():
    session.pop('user_id', None)
    return redirect('/login')


# user
@app.route("/user/id/<id>", methods=["GET"])
def get_user_page(id):
    if not is_exists_user_session(id):
        return redirect("/login")

    user = db.get_or_404(User, id)

    return render_template('userpage.html', user=user)


@app.route('/user/create', methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        error_messages = []

        if db.session.execute(db.select(User).where(User.username == request.form["username"])).first():
            error_messages.append("User with this username already exists")
        elif request.form["password"] != request.form["confirm_password"]:
            error_messages.append("Passwords do not match")

        user = User(request.form["username"],
                    request.form["password"],
                    request.form["email"],
                    request.form["fio"],
                    request.form["sex"],
                    validator.convert_string_to_date(request.form["date_of_birth"]),
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
        return redirect("/login")

    return render_template('create_user_account.html')


@app.route("/user/id/<id>/update", methods=["GET", "POST"])
def update_user(id):
    if not is_exists_user_session(id):
        return redirect("/login")

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

        new_user = User(user.username,
                        password,
                        request.form["email"],
                        request.form["fio"],
                        request.form["sex"],
                        validator.convert_string_to_date(request.form["date_of_birth"]),
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
        return redirect(f"/user/id/{user.id}")
    
    return render_template('update_userdata.html', user=user)


# not implemented
@app.route("/user/id/<id>/delete", methods=["POST"])
def delete_user(id):
    pass


@app.route("/user/id/<id>/skills", methods=["GET"])
def get_users_skills_page(id):
    if not is_exists_user_session(id):
        return redirect("/login")

    user = db.get_or_404(User, id)

    return render_template('projects.html', user_id=id, projects=user.skills)


# not implemented
@app.route("/user/id/<id>/requests", methods=["GET"])
def get_users_requests_page(id):
    pass


@app.route("/user/id/<id>/projects", methods=["GET"])
def get_users_projects_page(id):
    if not is_exists_user_session(id):
        return redirect("/login")

    user = db.get_or_404(User, id)

    return render_template('projects.html', user_id=id, projects=user.projects_participated)


# skills
# not implemented
@app.route("/user/id/<id>/skill/<skill_id>", methods=["GET"])
def get_skill_page(id, skill_id):
    pass


# not implemented
@app.route("/user/id/<id>/skill/create", methods=["GET", "POST"])
def create_skill(id):
    pass


# not implemented
@app.route("/user/id/<id>/skill/<skill_id>/update", methods=["GET", "POST"])
def update_skill(id, skill_id):
    pass


# not implemented
@app.route("/user/id/<id>/skill/<skill_id>/delete", methods=["POST"])
def delete_skill(id, skill_id):
    pass


# request
# not implemented
@app.route("/user/id/<id>/request/<request_id>", methods=["GET"])
def get_request_page(id, request_id):
    pass


# not implemented
@app.route("/user/id/<id>/request/create", methods=["GET", "POST"])
def create_request(id):
    pass


# not implemented
@app.route("/user/id/<id>/request/<request_id>/update", methods=["GET", "POST"])
def update_request(id, request_id):
    pass


# not implemented
@app.route("/user/id/<id>/request/<request_id>/delete", methods=["POST"])
def delete_request(id, request_id):
    pass


# project
# not implemented
@app.route("/project/id/<id>", methods=["GET"])
def get_project_page(id):
    pass


# not implemented
@app.route("/project/create", methods=["GET", "POST"])
def create_project():
    pass


# not implemented
@app.route("/project/id/<id>/update", methods=["GET", "POST"])
def update_project(id):
    pass


# not implemented
@app.route("/project/id/<id>/delete", methods=["POST"])
def delete_project(id):
    pass


# project status
# not implemented
@app.route("/project_status/id/<id>", methods=["GET"])
def get_project_status_page(id):
    pass


# not implemented
@app.route("/project_status/create", methods=["GET", "POST"])
def create_project_status():
    pass


# not implemented
@app.route("/project_status/id/<id>/update", methods=["GET", "POST"])
def update_project_status(id):
    pass


# not implemented
@app.route("/project_status/id/<id>/delete", methods=["POST"])
def delete_project_status(id):
    pass


# company
# not implemented
@app.route("/company/id/<id>", methods=["GET"])
def get_company_page(id):
    pass


# not implemented
@app.route("/company/create", methods=["GET", "POST"])
def create_company():
    pass


# not implemented
@app.route("/company/id/<id>/update", methods=["GET", "POST"])
def update_company(id):
    pass


# not implemented
@app.route("/company/id/<id>/delete", methods=["POST"])
def delete_company(id):
    pass


# other utils
def is_exists_user_session(id):
    if "user_id" not in session:
        return False

    if session["user_id"] != int(id):
        return False

    return True