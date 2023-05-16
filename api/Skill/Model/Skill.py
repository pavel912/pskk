import datetime as dt
from api.Social.Model.Associations import tie_user_skill, tie_company_skill, tie_project_skill
from sqlalchemy import Column, String, Integer, DATETIME
from sqlalchemy.orm import relationship
from db import db
from utils.SessionsUtils import to_json


class Skill(db.Model):
    id = Column(Integer, primary_key=True)

    name = Column(String(256))

    skill_type = Column(String(64))

    status = Column(String(64))  # approved or not

    description = Column(String(256))

    created_at = Column(DATETIME)

    users = relationship("User", secondary=tie_user_skill, back_populates='skills', lazy="joined")

    companies = relationship("Company", secondary=tie_company_skill, back_populates='skills', lazy="joined")

    projects = relationship("Project", secondary=tie_project_skill, back_populates='required_skills', lazy="joined")

    def __repr__(self):
        return to_json(self)

    def __init__(self, name: str, skill_type: str, status: str, description: str = '', users: list = None,
                 companies: list = None, projects: list = None, id: int = None,
                 created_at: dt.datetime = dt.datetime.now()):
        self.name = name
        self.skill_type = skill_type
        self.status = status
        self.created_at = created_at
        self.description = description
        self.users = users if users else list()
        self.companies = companies if companies else list()
        self.projects = projects if projects else list()
        self.id = id if id else self.id
