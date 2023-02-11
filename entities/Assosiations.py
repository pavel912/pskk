from sqlalchemy import Table, ForeignKey, Column
from entities.Base import Base

user_project = Table(
    "user_project",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)

user_skill = Table(
    "user_skill",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)

legal_project = Table(
    "legal_project",
    Base.metadata,
    Column("legal_id", ForeignKey("legal_user.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)

user_skill = Table(
    "legal_skill",
    Base.metadata,
    Column("legal_id", ForeignKey("legal_user.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)


project_skill = Table(
    "project_skill",
    Base.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)