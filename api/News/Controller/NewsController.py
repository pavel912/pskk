import json

from News.Model.News import News
from db import db
from flask import Blueprint, request
from utils.SessionsUtils import build_response
from utils.TokenUtils import token_required, admin_only

news_app = Blueprint("news",
                     __name__,
                     url_prefix="/api/news/")


@news_app.route("", methods=["GET"])
def get_all_news():
    news = [str(new) for new in db.session.execute(db.select(News).order_by(News.created_at.desc()).limit(3)).scalars()]
    return build_response(news, 200)


@news_app.route("<id>/", methods=["GET"])
def get_news_by_id(id):
    news = db.get_or_404(News, int(id))
    return build_response(str(news), 200)


@news_app.route("", methods=["POST"])
@token_required
@admin_only
def create_news():
    form = request.get_json()

    news = News(
        form['title'],
        form['body'],
        form['image_path'])

    db.session.add(news)
    db.session.commit()

    return build_response(f"'Created news with id': {news.id}", 201)


@news_app.route("<id>/", methods=["PUT"])
@token_required
@admin_only
def update_news(id):
    news_old = db.get_or_404(News, id)

    form = request.get_json()

    news = News(
        form['title'],
        form['body'],
        form['image_path'],
        created_at=news_old.created_at,
        id=news_old.id)

    db.session.delete(news_old)
    db.session.add(news)
    db.session.commit()

    return build_response("{}", 200)


@news_app.route("<id>/", methods=["DELETE"])
@token_required
@admin_only
def delete_news(id):
    news = db.get_or_404(News, id)

    db.session.delete(news)
    db.session.commit()

    return build_response("{}", 200)
