from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import Session, Query
import datetime as dt
from entities.User import User
from entities.Project import Project
from entities.Base import Base


class DB_Handler:
    def __init__(self):
        self.engine = create_engine("sqlite:///db/pskk_db", echo=True, future=True)

        session = Session(self.engine)
        session.execute("DROP TABLE IF EXISTS user;")
        session.execute("DROP TABLE IF EXISTS project;")
        session.execute("DROP TABLE IF EXISTS user_project;")
        session.commit()
        session.close()

        Base.metadata.create_all(self.engine)

    def create_user(self, user: User) -> bool:
        session = Session(self.engine)

        session.add(user)

        session.commit()
        session.close()

        return True
    
    def update_user(self, user: User) -> bool:
        session = Session(self.engine)

        user_dict = user.__dict__
        user_dict.pop("_sa_instance_state")

        query = update(User).values(user_dict).where(User.id == user.id)

        session.execute(query)

        session.commit()
        session.close()

        return True

    def get_user_by_username_and_password(self, user: User) -> User:

        session = Session(self.engine)

        query = select(User).where((User.username == user.username) & (User.password == user.password))

        user_return = session.execute(query).one_or_none()

        session.close()

        if user_return:
            return user_return[0]

        return user_return
    
    def get_user_by_id(self, id: int) -> User:
        session = Session(self.engine)

        query = select(User).where(User.id == id)

        user_return = session.execute(query).one_or_none()

        session.close()

        if user_return:
            return user_return[0]

        return user_return

    def is_unique_username(self, username: str) -> bool:
        session = Session(self.engine)

        query = select(User).where(User.username == username)

        any_user = session.execute(query).first()

        session.close()

        if any_user:
            return False

        return True
    
    def is_unique_password(self, password: str) -> bool:
        session = Session(self.engine)

        query = select(User).where(User.password == password)

        any_user = session.execute(query).first()

        session.close()

        if any_user:
            return False

        return True
    
    def get_users_projects(self, id: int) -> list:
        session = Session(self.engine)

        query = select(User).where(User.id == id)

        user_return = session.execute(query).one_or_none()

        projects = None

        if user_return:
            projects = user_return[0].projects
        
        session.close()

        return projects
    
    def create_project(self, project: Project) -> bool:
        session = Session(self.engine)

        session.add(project)

        session.commit()
        session.close()

        return True


    def add_test_data(self):
        user1 = User("bob", "bob", "bob@mail.ru", "Bob", "Bobob", "Bobich", dt.date(2001, 4, 18), "Analyst", "Ozon")
        user2 = User("bib", "bib", "bib@mail.ru", "Bib", "Bibib", "Bibich", dt.date(2001, 4, 19), "Dev", "Zozon")

        project1 = Project("project1", "Industry", "Nice project", dt.date(2020, 1, 1))
        project2 = Project("project2", "Commerce", "Great project", dt.date(2021, 1, 1))

        user1.projects += [project1, project2]
        user2.projects.append(project2)

        #project1.users.append(user1)
        #project2.users += [user1, user2]

        self.create_user(user1)
        self.create_user(user2)

        self.create_project(project1)
        self.create_project(project2)
