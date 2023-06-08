from flask import Flask, redirect
from News.Controller.NewsController import news_app
from Company.Controller.CompanyController import company_app
from Project.Controller.ProjectController import project_app
from Request.Controller.RequestController import request_app
from Skill.Controller.SkillController import skill_app
from User.Controller.UserController import user_app
from User.Controller.LoginController import login_app
import os


def create_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # replace it later for safety issues
    app.config.from_object(__name__)

    for bp in [news_app,
               company_app,
               project_app,
               request_app,
               skill_app,
               user_app,
               login_app]:
        app.register_blueprint(bp)

    return app


app = create_app()
port = 5001


@app.route("/", methods=["GET"])
def index():
    return redirect("/news/")

app.run(port=port, debug=True)
