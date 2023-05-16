from sqlalchemy import Column, Integer, String, DATETIME
from db import db
import datetime as dt
from utils.SessionsUtils import to_json


class Request(db.Model):
    id = Column(Integer, primary_key=True)

    request_type = Column(String(32))

    request_status = Column(String(32))

    created_at = Column(DATETIME)

    def __repr__(self):
        return to_json(self)

    def __init__(self,
                 request_type,
                 request_status,
                 id: int = None,
                 created_at: dt.datetime = dt.datetime.now()):
        self.request_type = request_type
        self.request_status = request_status
        self.id = id,
        self.created_at = created_at
