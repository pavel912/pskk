import datetime as dt
from Social.Model.Associations import tie_company_skill, tie_company_project, tie_user_company
from sqlalchemy import Column, String, Integer, DATE, DATETIME, ForeignKey
from sqlalchemy.orm import relationship
from db import db

from utils.SessionsUtils import to_json


class Company(db.Model):

    id = Column(Integer, primary_key=True)

    company_name = Column(String(256))

    email = Column(String(64))

    phone_number = Column(String(32))

    representative_fio = Column(String(256))

    superuser_id = Column(Integer, ForeignKey("user.id"))

    superuser = relationship("User", back_populates="superuser_in_companies")

    address = Column(String(128))

    post_index = Column(String(32))

    inn = Column(String(16))  # INN of a company

    registered_as_company_at = Column(DATE)

    created_at = Column(DATETIME)  # date of registration on the platform

    users = relationship("User", secondary=tie_user_company, back_populates='companies', lazy="joined")

    skills = relationship("Skill", secondary=tie_company_skill, back_populates='companies', lazy="joined")

    projects = relationship("Project", secondary=tie_company_project, back_populates='companies', lazy="joined")

    def __repr__(self):
        return to_json(self)

    def __init__(self, company_name: str, email: str, phone_number: str, representative_fio: str,
                 superuser_id: int, address: str, post_index: int, inn: str, registered_as_company_at: dt.date,
                 users: list = None, skills: list = None, projects: list = None, id: int = None,
                 created_at: dt.datetime = dt.datetime.now()):
        self.company_name = company_name
        self.email = email
        self.phone_number = phone_number
        self.representative_fio = representative_fio
        self.superuser_id = superuser_id
        self.address = address
        self.post_index = post_index
        self.inn = inn
        self.registered_as_company_at = registered_as_company_at
        self.created_at = created_at
        self.users = users if users else list()
        self.skills = skills if skills else list()
        self.projects = projects if projects else list()
        self.id = id if id else self.id
