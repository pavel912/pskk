from flask import Flask, redirect
from api.News.Controller.NewsController import news_app
from api.Company.Controller.CompanyController import company_app
from api.News.Model.News import News
from api.Project.Controller.ProjectController import project_app
from api.ProjectStatus.Controller.ProjectStatusController import project_status_app
from api.Request.Controller.RequestController import request_app
from api.Skill.Controller.SkillController import skill_app
from api.User.Controller.UserController import user_app
from api.User.Controller.LoginController import login_app
from api.User.Model.User import User
from api.Social.Model.Role import Role
from db import db
import os
from utils.DataValidator import convert_string_to_date


def create_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # replace it later for safety issues
    app.config.from_object(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + '\db\pskk_db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    for bp in [news_app, company_app, project_app, project_status_app, request_app, skill_app, user_app, login_app]:
        app.register_blueprint(bp)

    db.init_app(app)

    return app


app = create_app()
port = 5000


@app.route("/", methods=["GET"])
def index():
    return redirect("/api/news")


"""
if __name__ == "main":
    app.run(port=port)

"""

# test data
with app.app_context():
    db.drop_all()
    db.create_all()

    # add roles
    user_role = Role("User")
    admin_role = Role("Admin")
    db.session.add(user_role)
    db.session.add(admin_role)
    db.session.commit()

    # add test data
    news1 = News("Foo bar", "Foo bar")
    news2 = News("Fuzz buzz", "Fuzz buzz")
    user = User("plobanov", "plobanov", "", "", convert_string_to_date(""), "", "", user_role)
    db.session.add(news1)
    db.session.add(news2)
    db.session.add(user)
    db.session.commit()
