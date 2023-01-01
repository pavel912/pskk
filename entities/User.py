from sqlalchemy import Column, Integer, String, DATE
from sqlalchemy.orm import declarative_base
import datetime as dt

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    username = Column(String(30))

    password = Column(String)

    email = Column(String)

    name = Column(String)

    surname = Column(String)

    fathers_name = Column(String)

    date_of_birth = Column(DATE)

    job_role = Column(String)

    company_name = Column(String)

    def __repr__(self):
        ...
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.email!r})"

    def __init__(self, username: str, password: str, email: str = '', name: str = '', surname: str = '', fathers_name: str = '', date_of_birth: dt.date = dt.date(1, 1, 1), job_role: str = '', company_name: str = ''):
        self.username = username
        self.password = password
        self.email = email
        self.name = name
        self.surname = surname
        self.fathers_name = fathers_name
        self.date_of_birth = date_of_birth
        self.job_role = job_role
        self.company_name = company_name

    def update_data(self, username: str, email: str = '', name: str = '', surname: str = '', fathers_name: str = '', date_of_birth: dt.date = dt.date(1, 1, 1), job_role: str = '', company_name: str = ''):
        self.username = username
        self.email = email
        self.name = name
        self.surname = surname
        self.fathers_name = fathers_name
        self.date_of_birth = date_of_birth
        self.job_role = job_role
        self.company_name = company_name

    def update_password(self, pasword: str):
        self.password = pasword
