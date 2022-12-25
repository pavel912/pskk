from User import User, Base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


class LoginHandler:
    def __init__(self):
        self.engine = create_engine("sqlite:///C:\\Users\\lob55\\PycharmProjects\\pythonProject\\db\\pskk_db", echo=True, future=True)
        Base.metadata.create_all(self.engine)

    def login(self, user: User) -> bool:
        return self.is_user_exists(user)

    def create_user(self, user: User) -> bool:
        if self.is_user_exists(user):
            return False

        session = Session(self.engine)

        session.add(user)

        session.commit()
        session.close()

        return True

    def is_user_exists(self, user: User) -> bool:
        session = Session(self.engine)

        query = select(User).where((User.username == user.username) & (User.password == user.password))

        user = session.execute(query).one_or_none()

        session.close()

        if user:
            return True

        return False

    def add_test_users(self):
        user = User("admin", "admin")
        if not self.is_user_exists(user):
            session = Session(self.engine)
            session.add(user)

            session.commit()
            session.close()

