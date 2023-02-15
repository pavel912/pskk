from sqlalchemy import Column, ForeignKey, Table
from app_db import db

tie_user_project = Table(
    "tie_user_project",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)

tie_user_skill = Table(
    "tie_user_skill",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)

tie_company_project = Table(
    "tie_company_project",
    db.metadata,
    Column("company_id", ForeignKey("company.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)

tie_company_skill = Table(
    "tie_company_skill",
    db.metadata,
    Column("company_id", ForeignKey("company.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)

tie_user_company = Table(
    "tie_user_company",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("company_id", ForeignKey("company.id"), primary_key=True),
)

tie_project_skill = Table(
    "tie_project_skill",
    db.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("skill_id", ForeignKey("skill.id"), primary_key=True),
)
