import os

from api.News.Model.News import News
from flask import Blueprint, request
from db import db
from utils.SessionsUtils import build_response, is_admin

news_app = Blueprint("news",
                     __name__,
                     url_prefix="/api/news")


@news_app.route("/", methods=["GET"])
def get_all_news():
    news = [str(new) for new in db.session.execute(db.select(News).order_by(News.created_at.desc()).limit(3)).scalars()]
    return build_response(news, 200)


@news_app.route("/<id>", methods=["GET"])
def get_news_by_id(id):
    news = db.get_or_404(News, int(id))
    return build_response(str(news), 200)


@news_app.route("/", methods=["POST"])
def create_news():
    if not is_admin():
        return build_response(['Insufficient privileges'], 401)

    news = News(
        request.json['title'],
        request.json['body'],
        request.json['image_path'])

    db.session.add(news)
    db.session.commit()

    return build_response(f"'Created news with id': {news.id}", 201)


@news_app.route("/<id>", methods=["PUT"])
def update_news(id):
    if not is_admin():
        return build_response(['Insufficient privileges'], 401)

    news_old = db.get_or_404(News, id)

    news = News(
        request.json['title'],
        request.json['body'],
        request.json['image_path'],
        created_at=news_old.created_at,
        id=news_old.id)

    db.session.delete(news_old)
    db.session.add(news)
    db.session.commit()

    return build_response("{}", 200)


@news_app.route("/<id>", methods=["DELETE"])
def delete_news(id):
    if not is_admin():
        return build_response(['Insufficient privileges'], 401)

    news = db.get_or_404(News, id)

    db.session.delete(news)
    db.session.commit()

    return build_response("{}", 200)
