from flask import Flask, redirect
from MVC.News.Controller.NewsController import news_app
from MVC.Company.Controller.CompanyController import company_app
from MVC.News.Model.News import News
from MVC.Project.Controller.ProjectController import project_app
from MVC.ProjectStatus.Controller.ProjectStatusController import project_status_app
from MVC.Request.Controller.RequestController import request_app
from MVC.Skill.Controller.SkillController import skill_app
from MVC.User.Controller.UserController import user_app
from MVC.User.Controller.LoginController import login_app
from MVC.User.Model.User import User
from db import db
import os
from utils.DataValidator import convert_string_to_date

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # replace it later for safety issues
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + '\db\pskk_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

for bp in [news_app, company_app, project_app, project_status_app, request_app, skill_app, user_app, login_app]:
    app.register_blueprint(bp)

db.init_app(app)


@app.route("/", methods=["GET"])
def index():
    return redirect("/news")


# test data
with app.app_context():
    db.drop_all()
    db.create_all()

    # add test data
    news1 = News("Foo bar", "Foo bar")
    news2 = News("Fuzz buzz", "Fuzz buzz")
    user = User("plobanov", "plobanov", "", "", "", convert_string_to_date(""), "", "")
    db.session.add(news1)
    db.session.add(news2)
    db.session.add(user)
    db.session.commit()
