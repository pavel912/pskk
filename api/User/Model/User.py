import datetime as dt

from Social.Model.Associations import tie_user_company, tie_user_project, tie_user_skill
from sqlalchemy import Column, String, Integer, DATE, DATETIME, TEXT, ForeignKey
from sqlalchemy.orm import relationship
from db import db
from utils.SessionsUtils import to_json
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)

    email = Column(String(32))

    password = Column(String(32))

    fio = Column(String(256))

    date_of_birth = Column(DATE)

    sex = Column(String(8))

    source_of_knowing_about_pskk = Column(String(64))  # how is the company get familiar with pskk

    phone_number = Column(String(32))

    address = Column(String(256))

    post_index = Column(String(32))

    inn = Column(String(16))

    created_at = Column(DATETIME)

    occupation = Column(String(256))  # worker, self-employed etc

    company_name = Column(String(1024))

    about_me = Column(TEXT)

    companies = relationship("Company", secondary=tie_user_company, back_populates='users', lazy="joined")

    superuser_in_companies = relationship("Company", back_populates='users', lazy="joined")

    skills = relationship("Skill", secondary=tie_user_skill, back_populates='users', lazy="joined")

    projects_participated = relationship("Project", secondary=tie_user_project, back_populates='users', lazy="joined")

    projects_initiated = relationship("Project", back_populates='user_initiator', lazy="joined")

    role_id = Column(Integer, ForeignKey("role.id"))

    role = relationship('Role', uselist=False, back_populates="users", lazy="joined")

    documents = relationship('Document', back_populates="user", lazy="joined")

    def get(user_id):
        user = db.session.execute(db.select(User).where(User.id == int(user_id))).first()
        try:
            if len(user) > 0:
                return user[0]
            else:
                return None
        except:
            return user

    def __repr__(self):
        return to_json(self)

    def __init__(self, password: str, email: str, fio: str, sex: str, date_of_birth: dt.date,
                 source_of_knowing_about_pskk: str, phone_number: str, role, address: str = "", post_index: str = "",
                 inn: str = "", occupation: str = "", company_name: str = "", about_me: str = "",
                 companies: list = None, superuser_in_companies: list = None,
                 skills: list = None, projects_participated: list = None,
                 projects_initiated: list = None, documents: list = None,
                 id: int = None, created_at: dt.datetime = dt.datetime.now()):
        self.password = password
        self.email = email
        self.fio = fio
        self.sex = sex
        self.date_of_birth = date_of_birth
        self.source_of_knowing_about_pskk = source_of_knowing_about_pskk
        self.phone_number = phone_number
        self.role = role
        self.address = address
        self.post_index = post_index
        self.inn = inn
        self.occupation = occupation
        self.company_name = company_name
        self.created_at = created_at
        self.about_me = about_me
        self.companies = companies if companies else list()
        self.superuser_in_companies = superuser_in_companies if superuser_in_companies else list()
        self.skills = skills if skills else list()
        self.projects_participated = projects_participated if projects_participated else list()
        self.projects_initiated = projects_initiated if projects_initiated else list()
        self.documents = documents if documents else list()
        self.id = id if id else self.id