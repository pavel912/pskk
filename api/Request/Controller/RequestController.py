import json
import os

import requests
from flask import Blueprint, request
from db import db
from Request.Model.Request import Request
from utils.SessionsUtils import build_response
from utils.TokenUtils import token_required, admin_only

request_app = Blueprint(
    "request",
    __name__,
    url_prefix="/api/requests/")

entities = {
        "skill",
        "document"
    }


@request_app.route("", methods=["GET"])
@token_required
def get_all_requests():
    requests = [str(req) for req in Request.query.all()]

    return build_response(requests, 200)


@request_app.route("<id>/", methods=["GET"])
@token_required
def get_request_by_id(id):
    req = db.get_or_404(Request, id)

    return build_response(str(req), 200)


@request_app.route("", methods=["POST"])
@token_required
def create_request():
    form = json.loads(request.json)

    if form["entity_type"] not in entities:
        return build_response(f"'Entity {form['entity_type']} does not require validation'", 422)

    req = Request(
        form["type"],
        form["entity_type"],
        form["entity_id"]
    )

    db.session.add(req)
    db.session.commit()

    return build_response(f"'Created request with id': {req.id}", 201)


@request_app.route("<id>/", methods=["PUT"])
@token_required
@admin_only
def update_request(id):
    old_req = db.get_or_404(Request, id)

    form = json.loads(request.json)

    valid_statuses = {
        'In review',
        'Approved',
        'Declined'
    }

    if form["request_status"] not in valid_statuses:
        return build_response(f"'Request status {form['request_status']} is incorrect'", 422)

    if form["entity_type"] not in entities:
        return build_response(f"'Entity {form['entity_type']} does not require validation'", 422)

    req = Request(
        form["type"],
        form["entity_type"],
        form["entity_id"],
        id=old_req.id,
        request_status=form["request_status"],
        created_at=old_req.created_at
    )

    response = requests.get(f"http://localhost:5000/api/{req.entity_type}s/{req.entity_id}")

    if response.status_code >= 300:
        return build_response(f"'Failed to update request with id': {req.id}", 422)

    response_body = response.json()

    response_body['status'] = req.request_status

    response = requests.put(f"http://localhost:5000/api/{req.entity_type}s/{req.entity_id}",
                            json=json.dumps(response_body))

    if response.status_code >= 300:
        return build_response(f"'Failed to update request with id': {req.id}", 422)

    db.session.delete(old_req)
    db.session.add(req)
    db.session.commit()
    return build_response("{}", 200)


@request_app.route("<id>/", methods=["DELETE"])
@token_required
def delete_request(id):
    req = db.get_or_404(Request, id)

    db.session.delete(req)
    db.session.commit()

    return build_response("{}", 200)
