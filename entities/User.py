from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy.orm import relationship
import datetime as dt
from entities.Base import Base
from entities.Assosiations import user_project, user_skill

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    status = Column(String(30))

    username = Column(String(30))

    password = Column(String)

    email = Column(String)

    phone = Column(String(24))

    city = Column(String(64))

    index = Column(Integer)

    passport = Column(String(10))

    inn = Column(String(10))  # ИНН

    name = Column(String)

    surname = Column(String)

    fathers_name = Column(String)

    date_of_birth = Column(DATE)

    date_of_reg = Column(DATE) #date of registration

    num_of_projects = Column(Integer)

    job_role = Column(String)

    company_name = Column(String)

    come_from = Column(String(64)) #источник, благодаря которому узнали о ПСКК

    skills = relationship("Project", secondary=user_skill, back_populates='skills')

    projects = relationship("Project", secondary=user_project, back_populates='users')

    def __repr__(self):
        ...
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.email!r})"

    def __init__(self, username: str, password: str, email: str = '', phone: str = '', city: str = '', index: int = '',
                 passport: str = '', inn: str = '', name: str = '', surname: str = '', fathers_name: str = '',
                 date_of_birth: dt.date = dt.date(1, 1, 1),date_of_reg: dt.date = dt.date(1, 1, 1), num_of_projects: int = '',
                 job_role: str = '', company_name: str = '', come_from: str = '', skills = [], projects = []):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.city = city
        self.index = index
        self.passport = passport
        self.inn = inn
        self.name = name
        self.surname = surname
        self.fathers_name = fathers_name
        self.date_of_birth = date_of_birth
        self.date_of_reg = date_of_reg
        self.num_of_projects = num_of_projects
        self.job_role = job_role
        self.company_name = company_name
        self.come_from = come_from
        self.skills = skills
        self.projects = projects

    def update_data(self, username: str, email: str = '', name: str = '', surname: str = '', fathers_name: str = '',
                    date_of_birth: dt.date = dt.date(1, 1, 1), job_role: str = '', company_name: str = ''):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.fathers_name = fathers_name
        self.date_of_birth = date_of_birth
        self.job_role = job_role
        self.company_name = company_name

    def update_password(self, password: str):
        self.password = password
