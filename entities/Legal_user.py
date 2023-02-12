from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy.orm import relationship
import datetime as dt
from entities.Base import Base
from entities.Assosiations import user_project, user_skill

class User(Base):
    __tablename__ = "legal_user"

    id = Column(Integer, primary_key=True)

    username = Column(String(30))

    password = Column(String)

    email = Column(String)

    phone = Column(String(24))

    address = Column(String(128))

    index = Column(Integer)

    inn = Column(String(10))  # ИНН юрлиц

    company_name = Column(String)

    name = Column(String)

    surname = Column(String)

    fathers_name = Column(String)

    date_of_creation = Column(DATE)

    date_of_reg = Column(DATE) #date of registration on the platform

    num_of_projects = Column(Integer)

    come_from = Column(String(64)) #источник, благодаря которому узнали о ПСКК

    skills = relationship("Project", secondary=user_skill, back_populates='skills')

    projects = relationship("Project", secondary=user_project, back_populates='users')

    def __repr__(self):
        ...
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.email!r})"

    def __init__(self, username: str, password: str, email: str = '', phone: str = '', address: str = '', index: int = '', inn: str = '',
                 company_name: str = '', name: str = '', surname: str = '', fathers_name: str = '', date_of_creation: dt.date = dt.date(1, 1, 1),
                 date_of_reg: dt.date = dt.date(1, 1, 1), num_of_projects: int = '',  come_from: str = '', skills = [], projects = []):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.address = address
        self.index = index
        self.inn = inn
        self.company_name = company_name
        self.name = name
        self.surname = surname
        self.fathers_name = fathers_name
        self.date_of_creation = date_of_creation
        self.date_of_reg = date_of_reg
        self.num_of_projects = num_of_projects
        self.come_from = come_from
        self.skills = skills
        self.projects = projects

    def update_data(self, username: str, email: str = '', company_name: str = '', name: str = '', surname: str = '',
                    fathers_name: str = '', date_of_creation: dt.date = dt.date(1, 1, 1)):
        self.username = username
        self.email = email
        self.company_name = company_name
        self.name = name
        self.surname = surname
        self.fathers_name = fathers_name
        self.date_of_creation = date_of_creation

    def update_password(self, password: str):
        self.password = password
