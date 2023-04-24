from sqlalchemy import Column, Integer

from db import db


class Request(db.Model):
    id = Column(Integer, primary_key=True)
