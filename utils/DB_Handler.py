from entities.User import User, Base
from sqlalchemy import create_engine, select, update, func
from sqlalchemy.orm import Session, Query
import datetime as dt


class DB_Handler:
    def __init__(self):
        self.engine = create_engine("sqlite:///C:\\Users\\lob55\\PycharmProjects\\pythonProject\\db\\pskk_db", echo=True, future=True)

        session = Session(self.engine)
        session.execute("DROP TABLE IF EXISTS user;")
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


    def add_test_users(self):
        user1 = User("bob", "bob", "bob@mail.ru", "Bob", "Bobob", "Bobich", dt.date(2001, 4, 18), "Analyst", "Ozon")
        user2 = User("bib", "bib", "bib@mail.ru", "Bib", "Bibib", "Bibich", dt.date(2001, 4, 19), "Dev", "Zozon")

        self.create_user(user1)
        self.create_user(user2)
