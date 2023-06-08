import os

from flask import Blueprint, request
from db import db
from ProjectStatus.Model.ProjectStatus import ProjectStatus
from Project.Model.Project import Project
from utils.SessionsUtils import build_response
from utils.TokenUtils import token_required
import json

project_status_app = Blueprint(
    "project_status",
    __name__,
    url_prefix="/api/project_status/")


@project_status_app.route("", methods=["GET"])
@token_required
def get_all_project_statuses(id):
    statuses = [str(project_status) for project_status in ProjectStatus.query.all()]
    return build_response(statuses, 200)


@project_status_app.route("<id>/", methods=["GET"])
@token_required
def get_project_status_by_id(id):
    status = db.get_or_404(ProjectStatus, id)
    return build_response(str(status), 200)


@project_status_app.route("", methods=["POST"])
@token_required
def create_project_status():
    form = json.loads(request.json)

    project_status = ProjectStatus(
        form['name'],
        form['description']
    )

    db.session.add(project_status)
    db.session.commit()

    return build_response(f"'Created project status with id': {project_status.id}", 201)


@project_status_app.route("<id>/", methods=["PUT"])
@token_required
def update_project_status(id):
    project_status = db.get_or_404(ProjectStatus, id)

    form = json.loads(request.json)

    projects = [db.get_or_404(Project, project_id) for project_id in form['projects']]

    new_status = project_status = ProjectStatus(
        form['name'],
        form['description'],
        projects,
        id=project_status.id,
        created_at=project_status.created_at
    )

    db.session.delete(project_status)
    db.session.add(new_status)
    db.session.commit()

    return build_response("{}", 200)


@project_status_app.route("<id>/", methods=["DELETE"])
@token_required
def delete_project_status(id):
    project_status = db.get_or_404(ProjectStatus, id)

    db.session.delete(project_status)
    db.session.commit()

    return build_response("{}", 200)
