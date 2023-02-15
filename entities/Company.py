import datetime as dt
from entities.Associations import tie_company_skill, tie_company_project, tie_user_company
from sqlalchemy import Column, String, Integer, DATE, DATETIME
from sqlalchemy.orm import relationship
from app_db import db


class Company(db.Model):

    id = Column(Integer, primary_key=True)

    company_name = Column(String(256))

    email = Column(String(64))

    phone_number = Column(String(32))

    representative_fio = Column(String(256))

    address = Column(String(128))

    post_index = Column(String(32))

    inn = Column(String(16))  # INN of a company

    registered_as_company_at = Column(DATE)

    created_at = Column(DATETIME)  # date of registration on the platform

    source_of_knowing_about_pskk = Column(String(64))  # how is the company get familiar with pskk

    users = relationship("User", secondary=tie_user_company, back_populates='companies', lazy="joined")

    skills = relationship("Skill", secondary=tie_company_skill, back_populates='companies', lazy="joined")

    projects = relationship("Project", secondary=tie_company_project, back_populates='companies', lazy="joined")

    def __repr__(self):
        ...
        return f"Company(id={self.id!r}, company_name={self.company_name!r}, inn={self.inn!r})"

    def __init__(self, company_name: str, email: str, phone_number: str, representative_fio: str, address: str,
                 post_index: int, inn: str, registered_as_company_at: dt.date, source_of_knowing_about_pskk: str,
                 users: list = None, skills: list = None, projects: list = None, id: int = None,
                 created_at: dt.datetime = dt.datetime.now()):
        self.company_name = company_name
        self.email = email
        self.phone_number = phone_number
        self.representative_fio = representative_fio
        self.address = address
        self.post_index = post_index
        self.inn = inn
        self.registered_as_company_at = registered_as_company_at
        self.created_at = created_at
        self.source_of_knowing_about_pskk = source_of_knowing_about_pskk
        self.users = users if users else list()
        self.skills = skills if skills else list()
        self.projects = projects if projects else list()
        self.id = id if id else self.id
