import os

from MVC.News.Model.News import News
from flask import render_template, Blueprint
from db import db

news_app = Blueprint("news",
                     __name__,
                     url_prefix="/news",
                     template_folder=os.path.abspath(os.getcwd()) + '/MVC/News/View')


@news_app.route("/", methods=["GET"])
def get_all_news():
    news = db.session.execute(db.select(News).order_by(News.created_at.desc()).limit(3)).scalars()
    return render_template('index.html', news=news, bigheader=True)


@news_app.route("/<id>", methods=["GET"])
def get_news_by_id(id):
    news = db.get_or_404(News, int(id))
    return render_template('news.html', news=news)


# not implemented
@news_app.route("/create", methods=["GET", "POST"])
def create_news():
    pass


# not implemented
@news_app.route("/update/<id>", methods=["GET", "POST"])
def update_news(id):
    pass


# not implemented
@news_app.route("/delete/<id>", methods=["POST"])
def delete_news(id):
    pass
