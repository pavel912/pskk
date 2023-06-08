from flask import Flask, redirect
from News.Controller.NewsController import news_app
from Company.Controller.CompanyController import company_app
from News.Model.News import News
from Project.Controller.ProjectController import project_app
from ProjectStatus.Controller.ProjectStatusController import project_status_app
from Request.Controller.RequestController import request_app
from Skill.Controller.SkillController import skill_app
from User.Controller.UserController import user_app
from User.Controller.LoginController import login_app
from Document.Controller.DocumentController import document_app
from User.Model.User import User
from Social.Model.Role import Role
from db import db
import os
from utils.DataValidator import convert_string_to_date


def create_app():
    app = Flask("api")
    app.config['SECRET_KEY'] = "_5#y2LF4Q8z\n\xec]/"  # replace it later for safety issues
    app.config.from_object(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + '\db\pskk_db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    for bp in [
        news_app,
        company_app, 
        project_app,
        project_status_app, 
        request_app, 
        skill_app, 
        user_app, 
        login_app,
        document_app]:
        app.register_blueprint(bp)

    db.init_app(app)

    return app


app = create_app()
port = 5000


@app.route("/", methods=["GET"])
def index():
    return redirect("/api/news/")

app.run(port=port, debug=True)

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
    user = User("plobanov", "plobanov@mail.ru", "", "", convert_string_to_date(""), "", "", user_role)
    db.session.add(news1)
    db.session.add(news2)
    db.session.add(user)
    db.session.commit()
