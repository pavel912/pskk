from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from db import db

from utils.SessionsUtils import to_json


class Role(db.Model):
    id = Column(Integer, primary_key=True)

    name = Column(String(32))

    users = relationship('User', back_populates="role")

    def __repr__(self):
        return to_json(self)

    def __init__(self, name):
        self.name = name
