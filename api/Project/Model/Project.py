import datetime as dt
from Social.Model.Associations import tie_user_project, tie_project_skill, tie_company_project
from sqlalchemy import Column, String, Integer, DATE, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from db import db

from utils.SessionsUtils import to_json


class Project(db.Model):
    id = Column(Integer, primary_key=True)

    name = Column(String(256))

    user_initiator_id = Column(Integer, ForeignKey("user.id"))

    user_initiator = relationship("User", back_populates="projects_initiated")

    project_type = Column(String(64))

    description = Column(String(1024))

    created_at = Column(DATETIME)

    end_plan = Column(DATE)

    status_id = Column(Integer, ForeignKey("project_status.id"))

    status = relationship("ProjectStatus", back_populates="projects", lazy="joined")

    users = relationship("User", secondary=tie_user_project, back_populates='projects_participated', lazy="joined")

    companies = relationship("Company", secondary=tie_company_project, back_populates='projects', lazy="joined")

    required_skills = relationship("Skill", secondary=tie_project_skill, back_populates='projects', lazy="joined")

    def __repr__(self):
        return to_json(self)

    def __init__(self, name: str, user_initiator_id: int, project_type: str, description: str,
                 end_plan: dt.date,  status_id: int = None, users: list = None, companies: list = None, required_skills: list = None,
                 id: int = None, created_at: dt.datetime = dt.datetime.now()):
        self.name = name
        self.user_initiator_id = user_initiator_id
        self.project_type = project_type
        self.description = description
        self.created_at = created_at
        self.end_plan = end_plan
        self.status_id = status_id if status_id else 1
        self.users = users if users else list()
        self.companies = companies if companies else list()
        self.required_skills = required_skills if required_skills else list()
        self.id = id if id else self.id
