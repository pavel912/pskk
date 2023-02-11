from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy.orm import relationship
import datetime as dt
from entities.Base import Base
from entities.Assosiations import user_project, project_skill

class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)

    name = Column(String(256))

    initiator = Column(String(64))

    type = Column(String(64))

    description = Column(String(1024))

    created_at = Column(DATE)

    end_plan = Column(DATE)

    status = Column(String(64))

    skill_need = relationship("User", secondary=project_skill, back_populates='skills') #create relations with skills table

    users = relationship("User", secondary=user_project, back_populates='projects')

    def __repr__(self):
        ...
        return f"Project(id={self.id!r}, name={self.name!r}, created_at={self.created_at!r})"

    def __init__(self, name: str, initiator: str, type: str, description: str = '',
                 created_at: dt.date = dt.date(1, 1, 1), end_plan: dt.date = dt.date(1, 1, 1),
                 status: str = '', skill_need = [], users = []):
        self.name = name
        self.initiator = initiator
        self.type = type
        self.description = description
        self.created_at = created_at
        self.end_plan = end_plan
        self.status = status
        self.skill_need = skill_need
        self.users = users