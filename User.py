from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    username = Column(String(30))

    password = Column(String)

    email = Column(String)

    def __repr__(self):
        ...
        return f"User(id={self.id!r}, name={self.username!r}, fullname={self.email!r})"

    def __init__(self, username: str, password: str, email: str = ""):
        self.username = username
        self.password = password
        self.email = email


