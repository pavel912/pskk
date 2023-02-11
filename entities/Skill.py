from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy.orm import relationship
import datetime as dt
from entities.Base import Base
from entities.Assosiations import user_skill

class Project(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True)

    name = Column(String(256))

    type = Column(String(64))

    status = Column(String(64)) #approved or not

    users = relationship("Skill", secondary=user_skill, back_populates='users')

    def __repr__(self):
        ...
        return f"Project(id={self.id!r}, name={self.name!r}, created_at={self.created_at!r})"

    def __init__(self, name: str, type: str, description: str = '', status: str = '', users = []):
        self.name = name
        self.type = type
        self.description = description
        self.status = status
        self.users = users