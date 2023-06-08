import datetime as dt
from sqlalchemy import Column, String, Integer, DATETIME, ForeignKey
from sqlalchemy.orm import relationship

from User.Model.User import User
from db import db
from utils.SessionsUtils import to_json


class Document(db.Model):
    id = Column(Integer, primary_key=True)

    name = Column(String(256))

    path = Column(String(512))

    status = Column(String(64))

    created_at = Column(DATETIME)

    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates='documents', lazy="joined", uselist=False)

    def __repr__(self):
        return to_json(self)

    def __init__(self,
                 name: str,
                 path: str,
                 status: str,
                 user_id: int,
                 user: User = None,
                 id: int = None,
                 created_at: dt.datetime = dt.datetime.now()):
        self.name = name
        self.path = path
        self.status = status
        self.user_id = user_id
        self.user = user
        self.id = id if id else self.id
        self.created_at = created_at
