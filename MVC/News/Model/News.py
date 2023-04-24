import datetime as dt
from sqlalchemy import Column, String, Integer, DATETIME
from db import db


class News(db.Model):
    id = Column(Integer, primary_key=True)

    title = Column(String(256))

    body = Column(String(2048))

    image_path = Column(String(256))

    created_at = Column(DATETIME)

    def __repr__(self):
        ...
        return f"News(id={self.id!r}, title={self.title!r}, created_at={self.created_at!r})"

    def __init__(self, title: str, body: str, image_path: str = None,
                 id: int = None, created_at: dt.datetime = dt.datetime.now()):
        self.title = title
        self.body = body
        self.image_path = image_path
        self.created_at = created_at
        self.id = id if id else self.id
