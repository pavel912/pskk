import datetime as dt
from sqlalchemy import Column, String, Integer, DATETIME
from sqlalchemy.orm import relationship
from db import db
from utils.SessionsUtils import to_json


class ProjectStatus(db.Model):
    id = Column(Integer, primary_key=True)

    name = Column(String(32))

    description = Column(String(128))

    created_at = Column(DATETIME)

    projects = relationship("Project", back_populates='status', lazy="joined")

    def __repr__(self):
        return to_json(self)

    def __init__(self, name: str, description: str, projects: list = [],
                 id: int = None, created_at: dt.datetime = dt.datetime.now()):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.projects = projects if projects else list()
        self.id = id if id else self.id