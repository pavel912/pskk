import json
import os

import requests
from flask import Blueprint, request
from db import db
from api.Request.Model.Request import Request
from utils.SessionsUtils import build_response, is_admin

request_app = Blueprint(
    "request",
    __name__,
    url_prefix="/api/requests")

entities = {
        "skill",
        "document"
    }


@request_app.route("/", methods=["GET"])
def get_all_requests():
    requests = [str(req) for req in Request.query().all()]

    return build_response(requests, 200)


@request_app.route("/<id>", methods=["GET"])
def get_request_by_id(id):
    req = db.get_or_404(Request, id)

    return build_response(str(req), 200)


@request_app.route("/", methods=["POST"])
def create_request():
    if request.json["entity_type"] not in entities:
        return build_response(f"'Entity {request.json['entity_type']} does not require validation'", 422)

    req = Request(
        request.json["type"],
        request.json["entity_type"],
        request.json["entity_id"]
    )

    db.session.add(req)
    db.session.commit()

    return build_response(f"'Created request with id': {req.id}", 201)


@request_app.route("/<id>", methods=["PUT"])
def update_request(id):
    if not is_admin():
        return build_response(f"'Insufficient privileges'", 401)

    old_req = db.get_or_404(Request, id)

    valid_statuses = {
        'In review',
        'Approved',
        'Declined'
    }

    if request.json["request_status"] not in valid_statuses:
        return build_response(f"'Request status {request.json['request_status']} is incorrect'", 422)

    if request.json["entity_type"] not in entities:
        return build_response(f"'Entity {request.json['entity_type']} does not require validation'", 422)

    req = Request(
        request.json["type"],
        request.json["entity_type"],
        request.json["entity_id"],
        id=old_req.id,
        request_status=request.json["request_status"],
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


@request_app.route("/<id>", methods=["DELETE"])
def delete_request(id):
    req = db.get_or_404(Request, id)

    db.session.delete(req)
    db.session.commit()

    return build_response("{}", 200)
