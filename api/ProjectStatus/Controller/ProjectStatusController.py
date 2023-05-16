import os

from flask import Blueprint, request
from db import db
from api.ProjectStatus.Model.ProjectStatus import ProjectStatus
from api.Project.Model.Project import Project
from utils.SessionsUtils import is_exists_user_session, build_response, is_admin

project_status_app = Blueprint(
    "project_status",
    __name__,
    url_prefix="/api/project_status")


# not implemented
@project_status_app.route("/", methods=["GET"])
def get_all_project_statuses(id):
    statuses = [str(project_status) for project_status in ProjectStatus.query.all()]
    return build_response(statuses, 200)


@project_status_app.route("/<id>", methods=["GET"])
def get_project_status_by_id(id):
    status = db.get_or_404(ProjectStatus, id)
    return build_response(str(status), 200)


# not implemented
@project_status_app.route("/", methods=["POST"])
def create_project_status():
    project_status = ProjectStatus(
        request.json['name'],
        request.json['description']
    )

    db.session.add(project_status)
    db.session.commit()

    return build_response(f"'Created project status with id': {project_status.id}", 201)


# not implemented
@project_status_app.route("/<id>", methods=["PUT"])
def update_project_status(id):
    project_status = db.get_or_404(ProjectStatus, id)

    projects = [db.get_or_404(Project, project_id) for project_id in request.json['projects']]

    new_status = project_status = ProjectStatus(
        request.json['name'],
        request.json['description'],
        projects,
        id=project_status.id,
        created_at=project_status.created_at
    )

    db.session.delete(project_status)
    db.session.add(new_status)
    db.session.commit()

    return build_response("{}", 200)


# not implemented
@project_status_app.route("/delete/<id>", methods=["DELETE"])
def delete_project_status(id):
    project_status = db.get_or_404(ProjectStatus, id)

    db.session.delete(project_status)
    db.session.commit()

    return build_response("{}", 200)
