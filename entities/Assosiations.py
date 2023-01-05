from sqlalchemy import Table, ForeignKey, Column
from entities.Base import Base

user_project = Table(
    "user_project",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)